"""React Flow state machine with hierarchical state support."""

from typing import List, Union, Dict, Any
from transitions.extensions import GraphMachine
from .diagrams_reactflow import ReactFlowGraph


class ReactFlowMachine(GraphMachine):
    """
    State machine with React Flow graph generation support.

    Extends GraphMachine to generate graph data compatible with React Flow.
    Supports hierarchical states using a 'children' parameter in state definitions.

    Example:
        >>> states = [
        ...     'idle',
        ...     {'name': 'processing', 'children': ['validating', 'payment']},
        ...     'completed'
        ... ]
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'processing_validating'}
        ... ]
        >>> machine = ReactFlowMachine(states=states, transitions=transitions, initial='idle')
        >>> graph_data = machine.get_graph()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize React Flow state machine.

        Args:
            *args: Positional arguments passed to GraphMachine
            **kwargs: Keyword arguments passed to GraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super(ReactFlowMachine, self).__init__(*args, **kwargs)

    def add_states(
        self,
        states: Union[List[Union[str, Dict[str, Any]]], str, Dict[str, Any]],
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Add states to the machine with support for hierarchical state definitions.

        Processes state definitions that include a 'children' parameter to create
        hierarchical state names (e.g., 'parent_child'). Parent states are only
        added if they're explicitly used in transitions.

        Args:
            states: State definition(s). Can be:
                   - String: simple state name
                   - Dict: state config, may include 'children' for hierarchy
                   - List: multiple state definitions
            *args: Additional positional arguments for parent add_states
            **kwargs: Additional keyword arguments for parent add_states

        Raises:
            ValueError: If state definition is malformed

        Example:
            >>> machine.add_states([
            ...     'idle',
            ...     {'name': 'error', 'children': ['validation', 'payment']}
            ... ])
            # Creates states: 'idle', 'error', 'error_validation', 'error_payment'
        """
        # Normalize to list
        if not isinstance(states, list):
            states = [states]

        processed_states: List[Union[str, Dict[str, Any]]] = []

        for state in states:
            if isinstance(state, dict) and 'children' in state:
                # Handle hierarchical state
                parent_name = state.get('name')

                if not parent_name:
                    raise ValueError(
                        "State with 'children' must have a 'name' field")

                children = state.get('children', [])

                if not isinstance(children, list):
                    raise ValueError(
                        f"'children' for state '{parent_name}' must be a list")

                # Add parent state (will be filtered out by graph if unused)
                parent_state = {k: v for k,
                                v in state.items() if k != 'children'}
                processed_states.append(parent_state)

                # Add child states with hierarchical naming
                for child in children:
                    if isinstance(child, str):
                        processed_states.append(f"{parent_name}_{child}")
                    elif isinstance(child, dict):
                        # Child is a dict, merge with parent prefix
                        child_name = child.get('name')
                        if not child_name:
                            raise ValueError(
                                f"Child state dict must have 'name': {child}")
                        child_copy = child.copy()
                        child_copy['name'] = f"{parent_name}_{child_name}"
                        processed_states.append(child_copy)
                    else:
                        raise ValueError(
                            f"Invalid child type for '{parent_name}': {type(child)}")
            else:
                # Simple state or dict without children
                processed_states.append(state)

        return super(ReactFlowMachine, self).add_states(processed_states, *args, **kwargs)

    def _init_graphviz_engine(self, graph_engine: str) -> type:
        """
        Initialize the graph engine.

        Args:
            graph_engine: Name of the graph engine to use

        Returns:
            Graph engine class
        """
        if graph_engine == 'react-flow':
            return ReactFlowGraph
        return super(ReactFlowMachine, self)._init_graphviz_engine(graph_engine)
