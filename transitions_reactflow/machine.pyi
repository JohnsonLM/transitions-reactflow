"""Type stubs for ReactFlow machine classes."""

from typing import Any, Dict, List, Optional
from transitions.extensions import (
    GraphMachine,
    HierarchicalGraphMachine,
    LockedGraphMachine,
    LockedHierarchicalGraphMachine,
    AsyncGraphMachine,
    HierarchicalAsyncGraphMachine,
)


class ReactFlowMixin:
    def _init_graphviz_engine(self, graph_engine: str) -> type: ...


class ReactFlowMachine(ReactFlowMixin, GraphMachine):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class HierarchicalReactFlowMachine(ReactFlowMixin, HierarchicalGraphMachine):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class LockedReactFlowMachine(ReactFlowMixin, LockedGraphMachine):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class LockedHierarchicalReactFlowMachine(
    ReactFlowMixin, LockedHierarchicalGraphMachine
):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class AsyncReactFlowMachine(ReactFlowMixin, AsyncGraphMachine):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class HierarchicalAsyncReactFlowMachine(
    ReactFlowMixin, HierarchicalAsyncGraphMachine
):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...
