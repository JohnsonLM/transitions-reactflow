# transitions-reactflow

![Tests](https://github.com/JohnsonLM/transitions-reactflow/actions/workflows/test.yml/badge.svg)

React Flow graph engine for [pytransitions](https://github.com/pytransitions/transitions) state machines.

## Installation

```bash
pip install transitions-reactflow
```

## Quick Start

```python
from transitions_reactflow import ReactFlowMachine

states = ['idle', 'running', 'stopped']
transitions = [
    {'trigger': 'start', 'source': 'idle', 'dest': 'running'},
    {'trigger': 'stop', 'source': 'running', 'dest': 'stopped'}
]

machine = ReactFlowMachine(
    states=states,
    transitions=transitions,
    initial='idle'
)
graph_data = machine.get_graph()
# Returns: {'nodes': [...], 'edges': [...]}
```

## Demo

See the [demo app](demo/) for complete examples including Flask backend for serving graph descriptions and React frontend for displaying the graphs.

Run the demo:
```bash
cd demo
npm i
npm run build
python server.py
```

Then visit `http://localhost:5050` to see examples for all machine extensions.


## Credits

Built on [pytransitions](https://github.com/pytransitions/transitions).
