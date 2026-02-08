"""Type stubs for transitions_reactflow package."""

from typing import Any, Dict, List, Optional, Union, Sequence, Collection
from transitions.core import StateConfig, CallbacksArg
from transitions.extensions import GraphMachine

__version__: str
__author__: str


class ReactFlowMachine(GraphMachine):
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

    def add_states(
        self,
        states: Union[Sequence[StateConfig], StateConfig],
        on_enter: CallbacksArg = ...,
        on_exit: CallbacksArg = ...,
        ignore_invalid_triggers: Optional[bool] = ...,
        **kwargs: Any
    ) -> None: ...
    def get_graph(self, title: Optional[str] = ..., roi_state: Optional[str]
                  = ...) -> Dict[str, List[Dict[str, Any]]]: ...


class ReactFlowGraph:
    machine: GraphMachine
    def __init__(self, machine: GraphMachine) -> None: ...
    def generate(self) -> None: ...
    def get_graph(self, title: Optional[str] = ..., roi_state: Optional[str]
                  = ...) -> Dict[str, List[Dict[str, Any]]]: ...

    def set_previous_transition(self, src: str, dst: str) -> None: ...
    def reset_styling(self) -> None: ...
    def set_node_style(self, state: Any, style: str) -> None: ...


__all__: List[str]
