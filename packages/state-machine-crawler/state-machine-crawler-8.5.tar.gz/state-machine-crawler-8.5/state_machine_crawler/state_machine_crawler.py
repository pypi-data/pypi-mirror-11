import re
import inspect
from collections import defaultdict

from .errors import TransitionError, DeclarationError, UnreachableStateError, NonExistentStateError, MultipleStatesError
from .blocks import State
from .logger import StateLogger
from .collection import StateCollection


def _find_shortest_path(graph, start, end, path=[], get_cost=len):
    """ Derived from `here <https://www.python.org/doc/essays/graphs/>`_

    Finds the shortest path between two states. Estimations are based on a sum of costs of all transitions.
    """
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = _find_shortest_path(graph, node, end, path, get_cost)
            if newpath:
                if not shortest or get_cost(newpath) < get_cost(shortest):
                    shortest = newpath
    return shortest


def _create_state_map(all_states):
    """ Returns a graph for state transitioning """
    state_map = defaultdict(set)
    for state in all_states:
        state_map[state] = state_map[state] or set()
        for next_state in state.outgoing:
            state_map[state].add(next_state)
        for prev_state in state.incoming:
            state_map[prev_state].add(state)
    return state_map


def _create_transition_map(all_states):
    transition_map = {}
    for state in all_states:
        for name in dir(state):
            attr = getattr(state, name)

            if not hasattr(attr, "@transition@"):
                continue

            if attr.source_state:
                transition_map[attr.source_state, state] = attr
            else:

                target = attr.target_state
                if target == "self":
                    target = state

                transition_map[state, target] = attr

    return transition_map


def _create_state_map_with_exclusions(graph, entry_point, state_exclusion_list=None,
                                      transition_exclusion_list=None,
                                      filtered_graph=None):
    """
    Creates a sub_graph of a @graph with an assumption that a bunch of nodes from @state_exclusion_list are not
    reachable
    """
    filtered_graph = filtered_graph or {}
    state_exclusion_list = state_exclusion_list or []
    transition_exclusion_list = transition_exclusion_list or []
    if entry_point in state_exclusion_list:
        return {}
    if entry_point in filtered_graph or entry_point not in graph:
        return filtered_graph
    filtered_graph[entry_point] = filtered_children = set()
    for child_node in graph[entry_point]:
        if (entry_point, child_node) in transition_exclusion_list:
            continue
        if _create_state_map_with_exclusions(graph, child_node, state_exclusion_list, transition_exclusion_list,
                                             filtered_graph):
            filtered_children.add(child_node)
    return filtered_graph


def _get_missing_nodes(graph, sub_graph, entry_point):
    """ Returns a set of nodes that are present in the @graph but are missing in the @sub_graph """
    all_nodes = set()

    def _add_nodes(parent):
        if parent in all_nodes:
            return
        all_nodes.add(parent)
        for child in graph.get(parent, []):
            _add_nodes(child)

    def _remove_nodes(parent):
        if parent not in all_nodes:
            return
        all_nodes.remove(parent)
        for child in sub_graph.get(parent, []):
            _remove_nodes(child)

    _add_nodes(entry_point)
    _remove_nodes(entry_point)

    return all_nodes


def _dfs(graph, start, visited=None):
    """ Recursive depth first search """
    visited = visited or []
    if start not in visited:
        visited.append(start)
    for node in set(graph[start]) - set(visited):
        _dfs(graph, node, visited)
    return visited


def _get_all_unreachable_nodes(graph, entry_point, state_exclusion_list, transition_exclusion_list):
    """ Given a @graph and a bunch of unreachable states in @state_exclusion_list calculates which other nodes cannot
    be reached
    """
    sub_graph = _create_state_map_with_exclusions(graph, entry_point, state_exclusion_list,
                                                  transition_exclusion_list)
    return _get_missing_nodes(graph, sub_graph, entry_point)


class StateMachineCrawler(object):
    """ The crawler is responsible for orchestrating the transitions of system's states

    system
        All transitions shall change the internal state of this object.
    initial_state
        The first real state of the system. It must define a transition from the StateMachineCrawler.EntryPoint
        otherwise the crawler won't be able to find its way through

    >>> scm = StateMachineCrawler(system_object, InitialState)
    """

    class EntryPoint(State):

        @classmethod
        def _create_transition(cls, source_state):
            def tempo(ep_instance):
                pass
            tempo.cost = 0
            tempo.target_state = cls
            tempo.source_state = source_state
            tempo.im_class = source_state
            tempo.original = tempo
            return tempo

        def verify(self):
            return True

    def __init__(self, system, initial_state):
        if not issubclass(initial_state, State):
            raise DeclarationError("%r is not a State subclass" % initial_state)
        self.clear()
        self._system = system
        self._initial_state = initial_state
        self._registered_states = set()
        self._current_state = self.EntryPoint
        self._reload_graphs()
        self.log = StateLogger()
        self._register_state(initial_state)

    def _reload_graphs(self):
        self._state_graph = _create_state_map(self._registered_states)

        # get rid of all the states that are not reachable from the initial one
        dropset = set()
        for target_state in self._state_graph:
            if target_state is self._initial_state:
                continue
            if not _find_shortest_path(self._state_graph, self._initial_state, target_state):
                dropset.add(target_state)
        for item in dropset:
            self._state_graph.pop(item)

        for source_state, target_states in self._state_graph.iteritems():
            target_states.add(self.EntryPoint)

        self._state_graph[self.EntryPoint] = {self._initial_state}

    def clear(self):
        self._registered_collections = set()
        self._next_state = None
        self._error_states = set()
        self._visited_states = set()
        self._visited_transitions = set()
        self._error_transitions = set()
        self._visited_states.add(self.EntryPoint)
        self._history = []

    @property
    def state(self):
        """ Represents a current state of the sytstem """
        return self._current_state

    def _err(self, target_state, msg):
        text = "Move from state %s to state %s has failed: %s." % (self._current_state, target_state, msg)
        text += "\nHistory: \n%s\n" % " -> ".join([hist.full_name for hist in self._history])
        raise TransitionError(text)

    def _do_step(self, next_state):
        if self._current_state is self.EntryPoint:
            self._history = []
        self._next_state = next_state
        transition = self.as_graph(True)[self._current_state.full_name]["transitions"][next_state.full_name]["_entry"]
        self.log.msg(self._current_state, self._next_state)
        self.log.transition()
        try:
            transition(transition.im_class(self._system))
            self._visited_transitions.add((self._current_state, next_state))
            transition_ok = True
            self.log.ok()
        except Exception:
            self._error_transitions.add((self._current_state, next_state))
            transition_ok = False
            self.log.nok()
            self.log.show_traceback()
        if not transition_ok:
            self._error_states = _get_all_unreachable_nodes(self._state_graph, self.EntryPoint,
                                                            set.union(self._error_states, {next_state}),
                                                            self._error_transitions)
            self._current_state = self.EntryPoint
            self._err(next_state, "transition failure")
        self.log.verification()
        try:
            next_state(self._system).verify()
            self.log.ok()
            self._current_state = next_state
            self._history.append(next_state)
            self._visited_states.add(next_state)
            self._next_state = None
        except Exception:
            self.log.nok()
            self.log.show_traceback()
            self._next_state = None
            self._error_states = _get_all_unreachable_nodes(self._state_graph, self.EntryPoint,
                                                            set.union(self._error_states, {next_state}),
                                                            self._error_transitions)

            # mark all outgoing transitions from error states as impossible
            for state in self._error_states:
                for target_state in self._state_graph[state]:
                    self._error_transitions.add((state, target_state))

            self._current_state = self.EntryPoint
            self._err(next_state, "verification failure")

    def _get_cost(self, states):
        """ Returns a cumulative cost of the whole chain of transitions """
        cost = 0
        cursor = states[0]
        for state in states[1:]:
            cost += self.as_graph(True)[cursor.full_name]["transitions"][state.full_name]["_entry"].cost
            cursor = state
        return cost

    def _existing_state(self, name):
        found = []
        for state in self._state_graph:
            if name in state.full_name:
                found.append(state)
        if not found:
            raise NonExistentStateError("State '{0}' was not registered.".format(name))
        elif len(found) > 1:
            raise MultipleStatesError("Multiple states match search criteria were found: {0}".format(found))
        else:
            return found[0]

    def move(self, state):
        """ Performs a transition from the current state to the state passed as an argument

        state (subclass of :class:`State <state_machine_crawler.State>`)
            target state of the system

        >>> scm.move(StateOne)
        >>> scm.state is StateOne
        True
        """
        if state is self.EntryPoint:
            self._next_state = None
            self._current_state = self.EntryPoint
            return
        elif isinstance(state, basestring):
            state = self._existing_state(state)
        elif state not in self._registered_states:
            raise NonExistentStateError("State {0} was not registered.".format(state))
        reachable_state_graph = _create_state_map_with_exclusions(self._state_graph,
                                                                  self.EntryPoint,
                                                                  self._error_states,
                                                                  self._error_transitions)
        shortest_path = _find_shortest_path(reachable_state_graph, self._current_state, state, get_cost=self._get_cost)
        if shortest_path is None:
            raise UnreachableStateError("There is no way to achieve state %r" % state)
        if state is self._current_state:
            next_states = [state]
        else:
            next_states = shortest_path[1:]
        for next_state in next_states:
            self._do_step(next_state)

    def verify_all_states(self, pattern=None, full=False):
        """
        Makes sure that all states can be visited. It uses a depth first search to find the somewhat the quickest path.

        pattern (str=None)
            visits only the states full names of which match the pattern
        full (bool=False)
            if True, not only all states are visited but also all transitions are exercised
        """

        all_states_to_check = _dfs(self._state_graph, self._initial_state)

        actual_states_to_check = []
        if pattern is None:
            actual_states_to_check = all_states_to_check
        else:
            for state in all_states_to_check:
                if re.match(pattern, state.full_name):
                    actual_states_to_check.append(state)

        def _handled_call(function):
            try:
                function()
            except TransitionError, e:
                self.log.err(e)
            except UnreachableStateError:  # pragma: no cover
                pass  # show must go on!

        for state in actual_states_to_check:
            if state in self._error_states or state in self._visited_states:
                continue
            _handled_call(lambda: self.move(state))

        if full:

            unexecuted_transitions = set()
            for source_state, target_states in self._state_graph.iteritems():
                for target_state in target_states:
                    transition = (source_state, target_state)
                    if transition not in set.union(self._error_transitions, self._visited_transitions):
                        if target_state is self.EntryPoint:
                            continue
                        if pattern and not (re.match(pattern, source_state.full_name) and
                                            re.match(pattern, target_state.full_name)):
                            continue
                        unexecuted_transitions.add(transition)

            # TODO: find the most optimal way to execute the rest of transitions

            for transition in unexecuted_transitions:

                def _call():
                    if transition[0] != self._current_state:
                        self.move(transition[0])
                    self._do_step(transition[1])

                _handled_call(_call)

        self.move(self.EntryPoint)
        if self._error_states:
            failed_states = map(str, self._error_states)
            raise TransitionError("Failed to visit the following states: %s" % ", ".join(sorted(failed_states)))

    def _register_state(self, state, refresh=True):
        if not (inspect.isclass(state) and issubclass(state, State)):
            raise DeclarationError("state {0} must be a subclass of State".format(state))
        if state is State:
            return
        self._registered_states.add(state)
        for state in state.incoming + state.outgoing:
            if state not in self._registered_states:
                self._register_state(state)
        if refresh:
            self._reload_graphs()

    def register_state(self, state):
        """
        Registeres a concrete state and all states related to it inside the state machine

        state (State subclass)

        >>> scm.register_state(SomeState)
        """
        self._register_state(state)

    def register_collection(self, state_collection):
        """
        Registeres all states in a given state collection

        state_collection (StateCollection instance)

        >>> scm.register_collection(state_collection)
        """
        if state_collection.name in self._registered_collections:
            raise DeclarationError("Collection called '{0}' was already registred.".format(state_collection.name))
        self._registered_collections.add(state_collection.name)

        for state in state_collection.states:
            self._register_state(state, False)
        for state in state_collection.related_states:
            self._register_state(state, False)
        self._reload_graphs()

    def register_module(self, module):
        """
        Registeres all states from a given Python module

        module (python module)

        >>> from foobar import module_with_states
        >>> scm.register_module(module_with_states)
        """
        self.register_collection(StateCollection.from_module(module))

    def _create_transition_dict(self, source, target, transition):
        failed = (source, target) in self._error_transitions or source in self._error_states or \
            target in self._error_states
        return {
            "_entry": transition,
            "current": self._current_state is source and self._next_state is target,
            "name": transition.original.__name__,
            "target": target.full_name,
            "source": source.full_name,
            "cost": transition.cost,
            "visited": (source, target) in self._visited_transitions,
            "failed": failed
        }

    def as_graph(self, include_entry_point=False):
        """
        Returns a full graph representation of the state machine as a dict

        include_entry_point (bool=False)
            If True, the graph shall include the initial entry point and all related transitions.
            If False, the initial entry point and all related transitions are excluded from the graph

        """
        states = {}

        for state in self._state_graph:
            states[state.full_name] = {
                "_entry": state,
                "name": state.full_name,
                "current": state is self._current_state,
                "next": state is self._next_state,
                "visited": state in self._visited_states,
                "failed": state in self._error_states,
                "transitions": {}
            }

        for (source, target), transition in _create_transition_map(self._registered_states).iteritems():
            states[source.full_name]["transitions"][target.full_name] = \
                self._create_transition_dict(source, target, transition)

        if include_entry_point:
            for state_info in states.itervalues():
                source = state_info["_entry"]
                state_info["transitions"][self.EntryPoint.full_name] = \
                    self._create_transition_dict(source, self.EntryPoint, self.EntryPoint._create_transition(source))

        return states
