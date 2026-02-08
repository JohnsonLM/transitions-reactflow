"""React Flow graph generation for pytransitions state machines."""

from typing import Dict, List, Any, Optional, Set
from transitions.extensions.diagrams_base import BaseGraph


class ReactFlowGraph(BaseGraph):
    """
    React Flow graph engine for pytransitions.

    Generates graph data in React Flow format with nodes and edges
    that can be directly consumed by React Flow visualization library.
    """

    def generate(self) -> None:
        """
        Required by BaseGraph interface.
        No binary image generation needed for React Flow.
        """
        pass

    def get_graph(self, title: Optional[str] = None, roi_state: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate React Flow compatible graph data.

        Args:
            title: Optional graph title (not used in React Flow output)
            roi_state: Optional region of interest state (not implemented)

        Returns:
            Dictionary with 'nodes' and 'edges' keys containing React Flow compatible data

        Raises:
            ValueError: If graph data is malformed or missing required fields
        """
        try:
            # _get_elements() handles the complex state/transition resolution
            states, transitions = self._get_elements()

            if not isinstance(states, list) or not isinstance(transitions, list):
                raise ValueError("Invalid states or transitions data from _get_elements()")

            # Build edges first to determine which states are actually used
            edges = self._build_edges(transitions)

            # Get all states that are actually used in transitions
            used_state_ids = self._get_used_state_ids(edges)

            # Only include states that are used in transitions
            nodes = self._build_nodes(states, used_state_ids)

            return {"nodes": nodes, "edges": edges}

        except Exception as e:
            # Re-raise with more context
            raise ValueError(f"Failed to generate React Flow graph: {str(e)}") from e

    def _build_edges(self, transitions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Build React Flow edges from transition data.

        Args:
            transitions: List of transition dictionaries

        Returns:
            List of edge dictionaries with unique IDs
        """
        edges = []
        edge_counter: Dict[str, int] = {}  # Track duplicate edges

        for transition in transitions:
            source = transition.get('source')
            target = transition.get('dest', source)
            trigger = transition.get('trigger', '')

            if not source or not target:
                continue  # Skip invalid transitions

            # Create unique edge ID even for duplicate source->target pairs
            edge_key = f"{source}-{target}"
            edge_count = edge_counter.get(edge_key, 0)
            edge_counter[edge_key] = edge_count + 1

            edge_id = f"e-{edge_key}-{edge_count}" if edge_count > 0 else f"e-{edge_key}"

            edges.append({
                "id": edge_id,
                "source": source,
                "target": target,
                "label": trigger
            })

        return edges

    def _get_used_state_ids(self, edges: List[Dict[str, Any]]) -> Set[str]:
        """
        Extract all state IDs that are referenced in edges.

        Args:
            edges: List of edge dictionaries

        Returns:
            Set of state IDs that appear in transitions
        """
        used_state_ids: Set[str] = set()

        for edge in edges:
            if 'source' in edge:
                used_state_ids.add(edge['source'])
            if 'target' in edge:
                used_state_ids.add(edge['target'])

        return used_state_ids

    def _build_nodes(self, states: List[Dict[str, Any]], used_state_ids: Set[str]) -> List[Dict[str, Any]]:
        """
        Build React Flow nodes from state data.

        Args:
            states: List of state dictionaries
            used_state_ids: Set of state IDs that should be included

        Returns:
            List of node dictionaries
        """
        nodes = []

        for state in states:
            state_name = state.get('name')

            if not state_name:
                continue  # Skip states without names

            # Only include states that are actually used in transitions
            if state_name not in used_state_ids:
                continue

            nodes.append({
                "id": state_name,
                "data": {"label": state.get('label', state_name)},
                "position": {"x": 0, "y": 0}
            })

        return nodes

    # Abstract requirements for BaseGraph - not used for React Flow
    def set_previous_transition(self, src: str, dst: str) -> None:
        """Set styling for previous transition (not implemented for React Flow)."""
        pass

    def set_node_style(self, state: str, style: str) -> None:
        """Set node styling (not implemented for React Flow)."""
        pass

    def reset_styling(self) -> None:
        """Reset graph styling (not implemented for React Flow)."""
        pass
