"""React Flow state machine extensions."""

from typing import Any
from transitions.extensions import (
    GraphMachine,
    HierarchicalGraphMachine,
    LockedGraphMachine,
    LockedHierarchicalGraphMachine,
    AsyncGraphMachine,
    HierarchicalAsyncGraphMachine,
)
from .diagrams_reactflow import ReactFlowGraph


class ReactFlowMixin:
    """
    Mixin to add React Flow graph generation support to state machines.

    This mixin provides the core functionality for integrating ReactFlowGraph
    with any transitions machine type. It handles the graph engine initialization.
    """

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
        return super()._init_graphviz_engine(graph_engine)  # type: ignore


class ReactFlowMachine(ReactFlowMixin, GraphMachine):
    """
    State machine with React Flow graph generation support.

    Extends GraphMachine to generate graph data compatible with React Flow.

    Example:
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
        ...     {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
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
        super().__init__(*args, **kwargs)


class HierarchicalReactFlowMachine(ReactFlowMixin, HierarchicalGraphMachine):
    """
    Hierarchical state machine with React Flow graph generation support.

    Combines HierarchicalGraphMachine with React Flow visualization.
    Supports nested hierarchical states with proper state inheritance.

    Example:
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'}
        ... ]
        >>> machine = HierarchicalReactFlowMachine(
        ...     states=states, transitions=transitions, initial='idle'
        ... )
        >>> graph_data = machine.get_graph()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize Hierarchical React Flow state machine.

        Args:
            *args: Positional arguments passed to HierarchicalGraphMachine
            **kwargs: Keyword arguments passed to HierarchicalGraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super().__init__(*args, **kwargs)


class LockedReactFlowMachine(ReactFlowMixin, LockedGraphMachine):
    """
    Thread-safe state machine with React Flow graph generation support.

    Combines LockedGraphMachine with React Flow visualization.
    All state transitions are protected by a reentrant lock.

    Example:
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
        ...     {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ... ]
        >>> machine = LockedReactFlowMachine(
        ...     states=states, transitions=transitions, initial='idle'
        ... )
        >>> graph_data = machine.get_graph()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize Locked React Flow state machine.

        Args:
            *args: Positional arguments passed to LockedGraphMachine
            **kwargs: Keyword arguments passed to LockedGraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super().__init__(*args, **kwargs)


class LockedHierarchicalReactFlowMachine(ReactFlowMixin, LockedHierarchicalGraphMachine):
    """
    Thread-safe hierarchical state machine with React Flow graph generation.

    Combines LockedHierarchicalGraphMachine with React Flow visualization.
    Supports nested hierarchical states with thread-safe transitions.

    Example:
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'}
        ... ]
        >>> machine = LockedHierarchicalReactFlowMachine(
        ...     states=states, transitions=transitions, initial='idle'
        ... )
        >>> graph_data = machine.get_graph()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize Locked Hierarchical React Flow state machine.

        Args:
            *args: Positional arguments passed to LockedHierarchicalGraphMachine
            **kwargs: Keyword arguments passed to LockedHierarchicalGraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super().__init__(*args, **kwargs)


class AsyncReactFlowMachine(ReactFlowMixin, AsyncGraphMachine):
    """
    Async state machine with React Flow graph generation support.

    Combines AsyncGraphMachine with React Flow visualization.
    All transitions are async and can be awaited.

    Example:
        >>> import asyncio
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
        ...     {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ... ]
        >>> machine = AsyncReactFlowMachine(
        ...     states=states, transitions=transitions, initial='idle'
        ... )
        >>> async def main():
        ...     await machine.start()
        ...     graph_data = machine.get_graph()
        >>> asyncio.run(main())
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize Async React Flow state machine.

        Args:
            *args: Positional arguments passed to AsyncGraphMachine
            **kwargs: Keyword arguments passed to AsyncGraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super().__init__(*args, **kwargs)


class HierarchicalAsyncReactFlowMachine(ReactFlowMixin, HierarchicalAsyncGraphMachine):
    """
    Async hierarchical state machine with React Flow graph generation.

    Combines HierarchicalAsyncGraphMachine with React Flow visualization.
    Supports nested hierarchical states with async transitions.

    Example:
        >>> import asyncio
        >>> states = ['idle', 'running', 'stopped']
        >>> transitions = [
        ...     {'trigger': 'start', 'source': 'idle', 'dest': 'running'}
        ... ]
        >>> machine = HierarchicalAsyncReactFlowMachine(
        ...     states=states, transitions=transitions, initial='idle'
        ... )
        >>> async def main():
        ...     await machine.start()
        ...     graph_data = machine.get_graph()
        >>> asyncio.run(main())
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize Hierarchical Async React Flow state machine.

        Args:
            *args: Positional arguments passed to HierarchicalAsyncGraphMachine
            **kwargs: Keyword arguments passed to HierarchicalAsyncGraphMachine.
                     'graph_engine' defaults to 'react-flow' if not specified.
        """
        kwargs.setdefault('graph_engine', 'react-flow')
        super().__init__(*args, **kwargs)
