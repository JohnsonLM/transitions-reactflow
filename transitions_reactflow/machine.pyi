"""Type stubs for ReactFlowMachine."""

from typing import Any, Dict, List, Optional, Union, Sequence
from transitions.core import StateConfig, CallbacksArg
from transitions.extensions import GraphMachine


class ReactFlowMachine(GraphMachine):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

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
