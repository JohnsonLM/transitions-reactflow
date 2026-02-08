"""Type stubs for ReactFlowGraph."""

from typing import Any, Dict, List, Optional, Set
from transitions.extensions.diagrams_base import BaseGraph

class ReactFlowGraph(BaseGraph):
    def generate(self) -> None: ...
    def get_graph(self, title: Optional[str] = ..., roi_state: Optional[str] = ...) -> Dict[str, List[Dict[str, Any]]]: ...