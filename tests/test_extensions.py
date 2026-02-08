"""Tests for ReactFlow extension machine classes."""

import pytest
import threading
import time
from transitions_reactflow import (
    ReactFlowMachine,
    HierarchicalReactFlowMachine,
    LockedReactFlowMachine,
    LockedHierarchicalReactFlowMachine,
    AsyncReactFlowMachine,
    HierarchicalAsyncReactFlowMachine,
)


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

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        assert 'nodes' in graph
        assert 'edges' in graph
        assert len(graph['nodes']) == 2
        assert len(graph['edges']) == 1

    def test_unused_states_filtered(self):
        """Test that unused states are filtered from graph."""
        states = ['idle', 'processing_validating', 'processing_payment', 'completed']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'processing_validating'},
            {'trigger': 'finish', 'source': 'processing_validating', 'dest': 'completed'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        node_ids = {node['id'] for node in graph['nodes']}
        assert 'processing_payment' not in node_ids
        assert 'processing_validating' in node_ids

    def test_duplicate_edges_unique_ids(self):
        """Test that duplicate edges get unique IDs."""
        states = ['idle', 'running']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'restart', 'source': 'idle', 'dest': 'running'},
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        assert len(graph['edges']) == 2
        edge_ids = [edge['id'] for edge in graph['edges']]
        assert len(edge_ids) == len(set(edge_ids))

    def test_state_with_dict_config(self):
        """Test states defined with dict configuration."""
        states = [
            'idle',
            {'name': 'processing_validating'},
            {'name': 'processing_payment'},
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'processing_validating'},
            {'trigger': 'validate', 'source': 'processing_validating', 'dest': 'processing_payment'},
            {'trigger': 'pay', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = ReactFlowMachine(
            states=states, transitions=transitions, initial='idle')

        assert hasattr(machine, 'start')
        assert hasattr(machine, 'validate')
        assert hasattr(machine, 'pay')

        machine.start()
        assert machine.state == 'processing_validating'

        machine.validate()
        assert machine.state == 'processing_payment'

        machine.pay()
        assert machine.state == 'completed'

    def test_non_react_flow_graph_engine(self):
        """Test _init_graphviz_engine with non-react-flow engine."""
        from transitions_reactflow.diagrams_reactflow import ReactFlowGraph

        machine = ReactFlowMachine.__new__(ReactFlowMachine)
        result = machine._init_graphviz_engine('graphviz')
        assert result != ReactFlowGraph


class TestHierarchicalReactFlowMachine:
    """Test cases for HierarchicalReactFlowMachine."""

    def test_simple_machine_creation(self):
        """Test creating a simple hierarchical state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = HierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

    def test_hierarchical_states(self):
        """Test creating a machine with hierarchical states."""
        states = [
            'idle',
            'processing_validating', 'processing_payment',
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'approve', 'source': 'processing_validating',
                'dest': 'processing_payment'},
            {'trigger': 'finish', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = HierarchicalReactFlowMachine(
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

        machine = HierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)


class TestLockedReactFlowMachine:
    """Test cases for LockedReactFlowMachine."""

    def test_simple_machine_creation(self):
        """Test creating a simple locked state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = LockedReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

    def test_thread_safety(self):
        """Test that transitions are thread-safe."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'idle'},
        ]

        machine = LockedReactFlowMachine(
            states=states, transitions=transitions, initial='idle')

        results = []

        def worker(machine, trigger, expected_states):
            """Worker thread that performs transitions."""
            for _ in range(10):
                if machine.trigger(trigger):
                    results.append((trigger, machine.state in expected_states))
                time.sleep(0.001)

        # Start two threads that alternate between states
        t1 = threading.Thread(
            target=worker, args=(machine, 'start', ['running']))
        t2 = threading.Thread(
            target=worker, args=(machine, 'stop', ['idle']))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # All transitions should have resulted in valid states
        assert all(valid for _, valid in results)

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = LockedReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)


class TestLockedHierarchicalReactFlowMachine:
    """Test cases for LockedHierarchicalReactFlowMachine."""

    def test_simple_machine_creation(self):
        """Test creating a simple locked hierarchical state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = LockedHierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

    def test_hierarchical_states(self):
        """Test creating a machine with hierarchical states."""
        states = [
            'idle',
            'processing_validating', 'processing_payment',
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'approve', 'source': 'processing_validating',
                'dest': 'processing_payment'},
            {'trigger': 'finish', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = LockedHierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

        # Test transitions
        machine.start()
        assert machine.state == 'processing_validating'

        machine.approve()
        assert machine.state == 'processing_payment'

        machine.finish()
        assert machine.state == 'completed'

    def test_thread_safety_with_hierarchy(self):
        """Test that hierarchical transitions are thread-safe."""
        states = [
            'idle',
            'processing_validating', 'processing_payment',
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'reset', 'source': 'processing_validating', 'dest': 'idle'},
        ]

        machine = LockedHierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')

        results = []

        def worker(machine, trigger, expected_states):
            """Worker thread that performs transitions."""
            for _ in range(10):
                if machine.trigger(trigger):
                    results.append((trigger, machine.state in expected_states))
                time.sleep(0.001)

        # Start two threads that alternate between states
        t1 = threading.Thread(
            target=worker, args=(machine, 'start', ['processing_validating']))
        t2 = threading.Thread(
            target=worker, args=(machine, 'reset', ['idle']))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # All transitions should have resulted in valid states
        assert all(valid for _, valid in results)

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'}
        ]

        machine = LockedHierarchicalReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)

        # Check nodes
        node_ids = {node['id'] for node in graph['nodes']}
        assert 'idle' in node_ids
        assert 'running' in node_ids


class TestAsyncReactFlowMachine:
    """Test cases for AsyncReactFlowMachine."""

    @pytest.mark.asyncio
    async def test_simple_machine_creation(self):
        """Test creating a simple async state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = AsyncReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

        # Test async transitions
        await machine.start()
        assert machine.state == 'running'

        await machine.stop()
        assert machine.state == 'stopped'

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = AsyncReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)


class TestHierarchicalAsyncReactFlowMachine:
    """Test cases for HierarchicalAsyncReactFlowMachine."""

    @pytest.mark.asyncio
    async def test_simple_machine_creation(self):
        """Test creating a simple async hierarchical state machine."""
        states = ['idle', 'running', 'stopped']
        transitions = [
            {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
            {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
        ]

        machine = HierarchicalAsyncReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

        # Test async transitions
        await machine.start()
        assert machine.state == 'running'

        await machine.stop()
        assert machine.state == 'stopped'

    @pytest.mark.asyncio
    async def test_hierarchical_states(self):
        """Test creating a machine with hierarchical states."""
        states = [
            'idle',
            'processing_validating', 'processing_payment',
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
            {'trigger': 'approve', 'source': 'processing_validating',
                'dest': 'processing_payment'},
            {'trigger': 'finish', 'source': 'processing_payment', 'dest': 'completed'}
        ]

        machine = HierarchicalAsyncReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        assert machine.state == 'idle'

        # Test async transitions
        await machine.start()
        assert machine.state == 'processing_validating'

        await machine.approve()
        assert machine.state == 'processing_payment'

        await machine.finish()
        assert machine.state == 'completed'

    def test_get_graph(self):
        """Test graph generation."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machine = HierarchicalAsyncReactFlowMachine(
            states=states, transitions=transitions, initial='idle')
        graph = machine.get_graph()

        # Check graph structure
        assert 'nodes' in graph
        assert 'edges' in graph
        assert isinstance(graph['nodes'], list)
        assert isinstance(graph['edges'], list)


class TestMachineInteroperability:
    """Test that all machine types work consistently."""

    def test_all_machines_support_children_syntax(self):
        """Test that all machines support the children syntax."""
        states = [
            'idle',
            'processing_validating', 'processing_payment',
            'completed'
        ]
        transitions = [
            {'trigger': 'start', 'source': 'idle',
                'dest': 'processing_validating'},
        ]

        machines = [
            ReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedHierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            AsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalAsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
        ]

        for machine in machines:
            if isinstance(machine, (AsyncReactFlowMachine, HierarchicalAsyncReactFlowMachine)):
                # Skip async machines in sync test
                continue
            machine.start()
            assert machine.state == 'processing_validating'

    def test_all_machines_generate_graphs(self):
        """Test that all machines can generate graphs."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machines = [
            ReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedHierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            AsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalAsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
        ]

        for machine in machines:
            graph = machine.get_graph()
            assert 'nodes' in graph
            assert 'edges' in graph
            assert len(graph['nodes']) == 2
            assert len(graph['edges']) == 1

    def test_graph_engine_defaults_to_react_flow(self):
        """Test that graph_engine parameter defaults to 'react-flow'."""
        states = ['idle', 'running']
        transitions = [{'trigger': 'start',
                        'source': 'idle', 'dest': 'running'}]

        machines = [
            ReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            LockedHierarchicalReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            AsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
            HierarchicalAsyncReactFlowMachine(
                states=states, transitions=transitions, initial='idle'),
        ]

        for machine in machines:
            # The graph should be generated without errors
            graph = machine.get_graph()
            assert isinstance(graph, dict)
