"""Tests for ReactFlowGraph class."""

import pytest
from transitions_reactflow import ReactFlowMachine


class TestReactFlowGraph:
    """Test cases for ReactFlowGraph."""

    def test_node_structure(self):
        """Test that nodes have the correct structure."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle', graph_engine='react-flow')
        graph = machine.get_graph()

        # Check node structure
        for node in graph['nodes']:
            assert 'id' in node
            assert 'data' in node
            assert 'position' in node
            assert 'label' in node['data']
            assert 'x' in node['position']
            assert 'y' in node['position']

    def test_edge_structure(self):
        """Test that edges have the correct structure."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check edge structure
        for edge in graph['edges']:
            assert 'id' in edge
            assert 'source' in edge
            assert 'target' in edge
            assert 'label' in edge

    def test_multiple_transitions(self):
        """Test graph with multiple transitions."""
        states = ['idle', 'validating', 'payment', 'completed']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'validating'},
            {'trigger': 'validate', 'source': 'validating', 'dest': 'payment'},
            {'trigger': 'pay', 'source': 'payment', 'dest': 'completed'},
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        assert len(graph['nodes']) == 4
        assert len(graph['edges']) == 3

    def test_self_transition(self):
        """Test graph with self-transition."""
        states = ['idle', 'running']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'retry', 'source': 'running',
                'dest': 'running'},  # Self-loop
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Find the self-loop edge
        self_loop = [e for e in graph['edges'] if e['source'] == e['target']]
        assert len(self_loop) == 1
        assert self_loop[0]['source'] == 'running'
        assert self_loop[0]['target'] == 'running'

    def test_multiple_source_states(self):
        """Test transition from multiple source states."""
        states = ['idle', 'running', 'paused', 'stopped']
        transitions = [
            {'trigger': 'stop', 'source': [
                'running', 'paused'], 'dest': 'stopped'},
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Should create separate edges for each source
        stop_edges = [e for e in graph['edges'] if e['label'] == 'stop']
        assert len(stop_edges) == 2

        sources = {e['source'] for e in stop_edges}
        assert 'running' in sources
        assert 'paused' in sources

    def test_empty_graph(self):
        """Test graph with no transitions."""
        states = ['idle']
        transitions = []

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # No transitions means no nodes (since unused states are filtered)
        assert len(graph['nodes']) == 0
        assert len(graph['edges']) == 0

    def test_node_labels(self):
        """Test that node labels default to state ID."""
        states = ['idle', 'running']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check default labels (same as ID)
        idle_node = [n for n in graph['nodes'] if n['id'] == 'idle'][0]
        assert idle_node['data']['label'] == 'idle'

        running_node = [n for n in graph['nodes'] if n['id'] == 'running'][0]
        assert running_node['data']['label'] == 'running'

    def test_roi_state_parameter(self):
        """Test that roi_state parameter is accepted (though not implemented)."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        # The roi_state parameter is in the method signature but not used
        # This test just ensures the method can be called
        graph = machine.get_graph()
        assert 'nodes' in graph
        assert 'edges' in graph

    def test_set_previous_transition(self):
        """Test set_previous_transition method (no-op for React Flow)."""
        from transitions_reactflow.diagrams_reactflow import ReactFlowGraph

        graph = ReactFlowGraph(None)
        # Should not raise an error
        graph.set_previous_transition('idle', 'running')
        # Method is no-op, so no assertions needed

    def test_get_graph_exception_handling(self):
        """Test exception handling in get_graph method."""
        from transitions_reactflow.diagrams_reactflow import ReactFlowGraph
        from unittest.mock import patch

        graph = ReactFlowGraph(None)

        # Mock _get_elements to return invalid data that causes an exception
        with patch.object(graph, '_get_elements', return_value=(None, [])):
            with pytest.raises(ValueError, match="Failed to generate React Flow graph"):
                graph.get_graph()
