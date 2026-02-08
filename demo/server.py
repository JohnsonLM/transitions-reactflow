from collections import OrderedDict
from flask import Flask, jsonify
from flask_cors import CORS
from transitions_reactflow import (
    ReactFlowMachine,
    HierarchicalReactFlowMachine,
    LockedReactFlowMachine,
    AsyncReactFlowMachine,
)

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# Demo 1: Traffic Light (ReactFlowMachine)
traffic_states = ['red', 'yellow', 'green']
traffic_transitions = [
    {'trigger': 'next', 'source': 'red', 'dest': 'green'},
    {'trigger': 'next', 'source': 'green', 'dest': 'yellow'},
    {'trigger': 'next', 'source': 'yellow', 'dest': 'red'},
    {'trigger': 'emergency', 'source': ['green', 'yellow'], 'dest': 'red'}
]

# Demo 2: User Authentication (LockedReactFlowMachine)
auth_states = [
    'logged_out',
    'checking_credentials',
    'mfa_required',
    'authenticated',
    'session_expired',
    'locked_out'
]
auth_transitions = [
    {'trigger': 'login', 'source': 'logged_out', 'dest': 'checking_credentials'},
    {'trigger': 'credentials_valid',
        'source': 'checking_credentials', 'dest': 'mfa_required'},
    {'trigger': 'credentials_invalid',
        'source': 'checking_credentials', 'dest': 'logged_out'},
    {'trigger': 'too_many_attempts',
        'source': 'checking_credentials', 'dest': 'locked_out'},
    {'trigger': 'mfa_success', 'source': 'mfa_required', 'dest': 'authenticated'},
    {'trigger': 'mfa_fail', 'source': 'mfa_required', 'dest': 'logged_out'},
    {'trigger': 'logout', 'source': 'authenticated', 'dest': 'logged_out'},
    {'trigger': 'session_timeout', 'source': 'authenticated', 'dest': 'session_expired'},
    {'trigger': 'relogin', 'source': 'session_expired',
        'dest': 'checking_credentials'},
    {'trigger': 'unlock', 'source': 'locked_out', 'dest': 'logged_out'}
]

# Demo 3: Device Connection (HierarchicalReactFlowMachine)
device_states = ['disconnected', 'connected', 'error']
device_transitions = [
    {'trigger': 'connect', 'source': 'disconnected', 'dest': 'connected'},
    {'trigger': 'disconnect', 'source': 'connected', 'dest': 'disconnected'},
    {'trigger': 'fail', 'source': '*', 'dest': 'error'},
    {'trigger': 'reset', 'source': 'error', 'dest': 'disconnected'}
]

# Demo 4: CI/CD Pipeline (AsyncReactFlowMachine)
cicd_states = [
    'idle',
    'building_compile',
    'building_test',
    'building_package',
    'deploying_staging',
    'deploying_production',
    'deployed',
    'failed_build_failed',
    'failed_test_failed',
    'failed_deploy_failed'
]
cicd_transitions = [
    {'trigger': 'start_build', 'source': 'idle', 'dest': 'building_compile'},
    {'trigger': 'compile_success', 'source': 'building_compile', 'dest': 'building_test'},
    {'trigger': 'compile_error', 'source': 'building_compile',
        'dest': 'failed_build_failed'},
    {'trigger': 'tests_pass', 'source': 'building_test', 'dest': 'building_package'},
    {'trigger': 'tests_fail', 'source': 'building_test', 'dest': 'failed_test_failed'},
    {'trigger': 'package_ready', 'source': 'building_package',
        'dest': 'deploying_staging'},
    {'trigger': 'staging_success', 'source': 'deploying_staging',
        'dest': 'deploying_production'},
    {'trigger': 'staging_failed', 'source': 'deploying_staging',
        'dest': 'failed_deploy_failed'},
    {'trigger': 'production_success',
        'source': 'deploying_production', 'dest': 'deployed'},
    {'trigger': 'production_failed', 'source': 'deploying_production',
        'dest': 'failed_deploy_failed'},
    {'trigger': 'rollback', 'source': 'deployed', 'dest': 'deploying_staging'},
    {'trigger': 'retry', 'source': [
        'failed_build_failed', 'failed_test_failed', 'failed_deploy_failed'], 'dest': 'idle'}
]


machines = OrderedDict([
    ('traffic', ReactFlowMachine(states=traffic_states,
     transitions=traffic_transitions, initial='red')),
    ('device', HierarchicalReactFlowMachine(states=device_states,
     transitions=device_transitions, initial='disconnected')),
    ('auth', LockedReactFlowMachine(states=auth_states,
     transitions=auth_transitions, initial='logged_out')),
    ('cicd', AsyncReactFlowMachine(states=cicd_states,
     transitions=cicd_transitions, initial='idle'))
])


graph_data = {
    name: {
        'graph': machine.get_graph(),
        'type': machine.__class__.__name__
    }
    for name, machine in machines.items()
}


@app.route('/graph-data')
def get_all_graph_data():
    """Serve all state machine graph data"""
    return jsonify({name: data['graph'] for name, data in graph_data.items()})


@app.route('/graph-data/<machine_name>')
def get_graph_data_by_name(machine_name):
    """Serve specific state machine graph data"""
    if machine_name in graph_data:
        return jsonify(graph_data[machine_name]['graph'])
    return jsonify({'error': 'Machine not found'}), 404


@app.route('/machines')
def get_machine_info():
    """Get information about all available machines (ordered list)"""
    return jsonify([
        {
            'id': name,
            'type': data['type'],
            'nodes': len(data['graph']['nodes']),
            'edges': len(data['graph']['edges'])
        }
        for name, data in graph_data.items()
    ])


@app.route('/')
def serve_index():
    """Serve the index.html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    print("Starting server at http://localhost:5050")
    print("\nEndpoints:")
    print("  • http://localhost:5050/ (react app)")
    print("  • http://localhost:5050/graph-data/<machine_name> (specific graph)")
    print("  • http://localhost:5050/graph-data (all graphs)")
    print("  • http://localhost:5050/machines (machine info)")
    app.run(debug=True, port=5050)
