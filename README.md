# transitions-reactflow
![example workflow](https://github.com/JohnsonLM/transitions-reactflow/actions/workflows/test.yml/badge.svg)

A React Flow graph engine extension for the [pytransitions](https://github.com/pytransitions/transitions) state machine library.

## Installation

```bash
pip install transitions-reactflow
```

Or install from source:

```bash
git clone https://github.com/johnsonlm/transitions-reactflow
cd transitions-reactflow
pip install -e .
```

## Quick Start

```python
from transitions_reactflow import ReactFlowMachine

# Define states with hierarchy
states = [
    'idle',
    {'name': 'processing', 'children': ['validating', 'payment']},
    'completed'
]

# Define transitions
transitions = [
    {'trigger': 'start', 'source': 'idle', 'dest': 'processing_validating'},
    {'trigger': 'validate', 'source': 'processing_validating', 'dest': 'processing_payment'},
    {'trigger': 'finish', 'source': 'processing_payment', 'dest': 'completed'}
]

# Create machine and get graph data
machine = ReactFlowMachine(states=states, transitions=transitions, initial='idle')
graph_data = machine.get_graph()

# Returns: {'nodes': [...], 'edges': [...]}
```

## Usage

### With Flask Backend

```python
from flask import Flask, jsonify
from flask_cors import CORS
from transitions_reactflow import ReactFlowMachine

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

machine = ReactFlowMachine(states=states, transitions=transitions, initial='idle')

@app.route('/graph-data')
def get_graph_data():
    return jsonify(machine.get_graph())
```

### With React Frontend

```javascript
import ReactFlow from 'reactflow';

function StateMachineFlow() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/graph-data').then(res => res.json()).then(setData);
  }, []);

  return data && <ReactFlow nodes={data.nodes} edges={data.edges} fitView />;
}
```

## Hierarchical States

Use `children` for nested states:

```python
states = [
    'idle',
    {'name': 'error', 'children': ['validation', 'payment', 'network']}
]
# Creates: error, error_validation, error_payment, error_network
```

**Note**: Unused parent states are automatically filtered from the graph.

## API

### ReactFlowMachine

Extends `transitions.extensions.GraphMachine`.

- `get_graph(title=None, roi_state=None)` → `{'nodes': [...], 'edges': [...]}`
- `add_states(states)`
- All standard pytransitions methods

### ReactFlowGraph

Extends `transitions.extensions.diagrams_base.BaseGraph`.

- `get_graph(title=None, roi_state=None)` → React Flow data
- Standard BaseGraph methods

## Graph Data Format

The `get_graph()` method returns React Flow compatible data:

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

```bash
# Tests
pytest tests/

# Coverage
pytest --cov=transitions_reactflow tests/

# Type checking
mypy transitions_reactflow/
```

## License

MIT - see LICENSE file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built on top of the [pytransitions](https://github.com/pytransitions/transitions) library.
