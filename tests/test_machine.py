"""Tests for ReactFlowMachine class."""

import pytest
from transitions_reactflow import ReactFlowMachine


class TestReactFlowMachine:
    """Test cases for ReactFlowMachine."""

    def test_simple_machine_creation(self):
        """Test creating a simple state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

    def test_hierarchical_states(self):
        """Test creating a machine with hierarchical states."""
        states = [
            'idle',
            {'name': 'processing', 'children': ['validating', 'payment']},
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'approve', 'source': 'processing_validating',
                'dest': 'processing_payment'},
            {'trigger': 'finish', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

        # Test transitions
        machine.start()
        assert machine.state == 'processing_validating'

        machine.approve()
        assert machine.state == 'processing_payment'

        machine.finish()
        assert machine.state == 'completed'

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)

        # Check nodes
        assert len(graph['nodes']) == 2
        node_ids = {node['id'] for node in graph['nodes']}
        assert 'idle' in node_ids
        assert 'running' in node_ids

        # Check edges
        assert len(graph['edges']) == 1
        edge = graph['edges'][0]
        assert edge['source'] == 'idle'
        assert edge['target'] == 'running'
        assert edge['label'] == 'start'

    def test_unused_parent_states_filtered(self):
        """Test that unused parent states are filtered from graph."""
        states = [
            'idle',
            {'name': 'processing', 'children': ['validating', 'payment']},
            'completed'
        ]
        # Note: 'processing' parent is never used directly in transitions
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'finish', 'source': 'processing_validating', 'dest': 'completed'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Parent 'processing' should not appear in nodes since it's unused
        node_ids = {node['id'] for node in graph['nodes']}
        assert 'processing' not in node_ids
        assert 'processing_validating' in node_ids

    def test_duplicate_edges_unique_ids(self):
        """Test that duplicate edges get unique IDs."""
        states = ['idle', 'running']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'restart', 'source': 'idle',
                'dest': 'running'},  # Same source->dest
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Both edges should be present with unique IDs
        assert len(graph['edges']) == 2
        edge_ids = [edge['id'] for edge in graph['edges']]
        assert len(edge_ids) == len(set(edge_ids))  # All IDs unique

    def test_invalid_state_with_children_no_name(self):
        """Test that state with children must have name."""
        states = [
            {'children': ['validating', 'payment']}  # Missing 'name'
        ]

        with pytest.raises(ValueError, match="must have a 'name' field"):
            ReactFlowMachine(states=states, transitions=[], initial='idle')

    def test_invalid_children_not_list(self):
        """Test that children must be a list."""
        states = [
            {'name': 'processing', 'children': 'not_a_list'}
        ]

        with pytest.raises(ValueError, match="must be a list"):
            ReactFlowMachine(states=states, transitions=[],
                             initial='processing')

    def test_hierarchical_states_with_dict_children(self):
        """Test hierarchical states where children are dict objects."""
        states = [
            'idle',
            {
                'name': 'processing',
                'children': [
                    {'name': 'validating'},
                    {'name': 'payment'}
                ]
            },
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'validate', 'source': 'processing_validating',
                'dest': 'processing_payment'},
            {'trigger': 'pay', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')

        # Test that states were created correctly
        assert hasattr(machine, 'start')
        assert hasattr(machine, 'validate')
        assert hasattr(machine, 'pay')

        # Test transitions work
        machine.start()
        assert machine.state == 'processing_validating'

        machine.validate()
        assert machine.state == 'processing_payment'

        machine.pay()
        assert machine.state == 'completed'

    def test_invalid_child_dict_without_name(self):
        """Test that child dict must have name."""
        states = [
            {
                'name': 'processing',
                'children': [
                    {'label': 'Validation'}  # Missing 'name'
                ]
            }
        ]

        with pytest.raises(ValueError, match="Child state dict must have 'name'"):
            ReactFlowMachine(states=states, transitions=[],
                             initial='processing')

    def test_invalid_child_type(self):
        """Test that invalid child types raise error."""
        states = [
            {
                'name': 'processing',
                'children': [123]  # Invalid type
            }
        ]

        with pytest.raises(ValueError, match="Invalid child type"):
            ReactFlowMachine(states=states, transitions=[],
                             initial='processing')

    def test_non_react_flow_graph_engine(self):
        """Test _init_graphviz_engine with non-react-flow engine."""
        from transitions_reactflow.diagrams_reactflow import ReactFlowGraph

        # This tests the fallback to parent class method
        machine = ReactFlowMachine.__new__(ReactFlowMachine)
        # Should not raise an error and return parent class result
        result = machine._init_graphviz_engine('graphviz')
        # We can't easily assert the exact return type, but it shouldn't be ReactFlowGraph
        assert result != ReactFlowGraph
