"""Type stubs for transitions_reactflow package."""

from typing import Any, Dict, List, Optional, Sequence
from transitions.core import StateConfig
from transitions.extensions import (
    GraphMachine,
    HierarchicalGraphMachine,
    LockedGraphMachine,
    LockedHierarchicalGraphMachine,
    AsyncGraphMachine,
    HierarchicalAsyncGraphMachine,
)

__version__: str
__author__: str


class ReactFlowMixin:
    def _init_graphviz_engine(self, graph_engine: str) -> type: ...


class ReactFlowMachine(ReactFlowMixin, GraphMachine):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class HierarchicalReactFlowMachine(ReactFlowMixin, HierarchicalGraphMachine):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class LockedReactFlowMachine(ReactFlowMixin, LockedGraphMachine):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class LockedHierarchicalReactFlowMachine(
    ReactFlowMixin, LockedHierarchicalGraphMachine
):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class AsyncReactFlowMachine(ReactFlowMixin, AsyncGraphMachine):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class HierarchicalAsyncReactFlowMachine(
    ReactFlowMixin, HierarchicalAsyncGraphMachine
):
    def __init__(
        self,
        model: Any = ...,
        states: Optional[Sequence[StateConfig]] = ...,
        transitions: Optional[List[Dict[str, Any]]] = ...,
        initial: Optional[str] = ...,
        model_attribute: str = ...,
        auto_transitions: bool = ...,
        title: str = ...,
        show_conditions: bool = ...,
        show_state_attributes: bool = ...,
        **kwargs: Any
    ) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...


class ReactFlowGraph:
    machine: GraphMachine

    def __init__(self, machine: GraphMachine) -> None: ...

    def generate(self) -> None: ...

    def get_graph(
        self, title: Optional[str] = ..., roi_state: Optional[str] = ...
    ) -> Dict[str, List[Dict[str, Any]]]: ...

    def set_previous_transition(self, src: str, dst: str) -> None: ...

    def reset_styling(self) -> None: ...

    def set_node_style(self, state: Any, style: str) -> None: ...


__all__: List[str]
