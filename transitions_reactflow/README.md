# transitions_reactflow

A React Flow graph engine extension for the [pytransitions](https://github.com/pytransitions/transitions) state machine library.

## Features

- ✅ **React Flow Compatible**: Generates graph data that can be directly consumed by React Flow
- ✅ **Hierarchical States**: Support for nested states using a `children` parameter
- ✅ **Smart Filtering**: Automatically filters out unused parent states from the graph
- ✅ **Unique Edge IDs**: Handles duplicate transitions with unique edge identifiers
- ✅ **Type Hints**: Fully typed with comprehensive type annotations
- ✅ **Error Handling**: Validates input and provides helpful error messages
- ✅ **Well Tested**: Comprehensive test suite included

## Installation

```bash
pip install transitions-rf
```

Or install from source:

```bash
git clone <repository-url>
cd transitions_reactflow
pip install -e .
```

## Quick Start

```python
from transitions_reactflow import ReactFlowMachine

# Define states with hierarchical structure
states = [
    'idle',
    {
        'name': 'processing',
        'children': ['validating', 'payment', 'fulfillment']
    },
    'completed'
]

# Define transitions
transitions = [
    {'trigger': 'start', 'source': 'idle', 'dest': 'processing_validating'},
    {'trigger': 'validate', 'source': 'processing_validating', 'dest': 'processing_payment'},
    {'trigger': 'pay', 'source': 'processing_payment', 'dest': 'processing_fulfillment'},
    {'trigger': 'finish', 'source': 'processing_fulfillment', 'dest': 'completed'}
]

# Create the machine
machine = ReactFlowMachine(
    states=states,
    transitions=transitions,
    initial='idle'
)

# Get React Flow compatible graph data
graph_data = machine.get_graph()

# Use in your React Flow application
print(graph_data)
# {
#   'nodes': [
#     {'id': 'idle', 'data': {'label': 'idle'}, 'position': {'x': 0, 'y': 0}},
#     ...
#   ],
#   'edges': [
#     {'id': 'e-idle-processing_validating', 'source': 'idle', 'target': 'processing_validating', 'label': 'start'},
#     ...
#   ]
# }
```

## Usage with Flask

```python
from flask import Flask, jsonify
from flask_cors import CORS
from transitions_reactflow import ReactFlowMachine

app = Flask(__name__)
CORS(app)

# Create your state machine
machine = ReactFlowMachine(states=states, transitions=transitions, initial='idle')
graph_data = machine.get_graph()

@app.route('/graph-data')
def get_graph_data():
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## React Flow Integration

On the frontend (React):

```javascript
import { useEffect, useState } from 'react';
import ReactFlow from 'reactflow';
import 'reactflow/dist/style.css';

export default function StateMachineFlow() {
  const [graphData, setGraphData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/graph-data')
      .then(res => res.json())
      .then(data => setGraphData(data));
  }, []);

  if (!graphData) return <div>Loading...</div>;

  return (
    <ReactFlow
      nodes={graphData.nodes}
      edges={graphData.edges}
      fitView
    />
  );
}
```

## Hierarchical States

The extension supports hierarchical states using a `children` parameter:

```python
states = [
    'idle',
    {
        'name': 'error',
        'children': ['validation_error', 'payment_error', 'network_error']
    }
]
```

This creates states: `error`, `error_validation_error`, `error_payment_error`, and `error_network_error`.

**Important**: Unused parent states are automatically filtered out of the graph. Only states that appear in transitions will be included in the output.

## API Reference

### ReactFlowMachine

Main class that extends `transitions.extensions.GraphMachine`.

**Constructor Parameters:**
- `states`: List of state definitions (strings or dicts)
- `transitions`: List of transition definitions
- `initial`: Initial state name
- `graph_engine`: Automatically set to 'react-flow' (optional)
- All other `GraphMachine` parameters

**Methods:**
- `get_graph(title=None, roi_state=None)`: Returns dict with `nodes` and `edges`
- `add_states(states)`: Add states with hierarchical support
- All standard pytransitions `Machine` methods

### Graph Data Format

**Nodes:**
```python
{
    "id": "state_name",
    "data": {"label": "state_name"},
    "position": {"x": 0, "y": 0}
}
```

**Edges:**
```python
{
    "id": "e-source-target",
    "source": "source_state",
    "target": "target_state",
    "label": "trigger_name"
}
```

## Development

### Running Tests

```bash
pip install pytest
pytest tests/
```

### Running with Coverage

```bash
pip install pytest-cov
pytest --cov=transitions_reactflow tests/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built on top of the excellent [pytransitions](https://github.com/pytransitions/transitions) library.
