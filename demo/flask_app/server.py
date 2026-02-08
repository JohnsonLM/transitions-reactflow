from flask import Flask, jsonify
from flask_cors import CORS
from transitions_reactflow.machine import ReactFlowMachine

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# Demo 1: E-commerce Order Processing
order_states = [
    'idle',
    {
        'name': 'processing',
        'children': ['validating', 'payment', 'fulfillment']
    },
    {
        'name': 'completed',
        'children': ['shipped', 'delivered']
    },
    {
        'name': 'error',
        'children': ['validation_error', 'payment_error', 'fulfillment_error']
    },
    'cancelled'
]

order_transitions = [
    {'trigger': 'start_order', 'source': 'idle',
        'dest': 'processing_validating'},
    {'trigger': 'validation_pass', 'source': 'processing_validating',
        'dest': 'processing_payment'},
    {'trigger': 'validation_fail', 'source': 'processing_validating',
        'dest': 'error_validation_error'},
    {'trigger': 'payment_approved', 'source': 'processing_payment',
        'dest': 'processing_fulfillment'},
    {'trigger': 'payment_declined', 'source': 'processing_payment',
        'dest': 'error_payment_error'},
    {'trigger': 'payment_retry', 'source': 'error_payment_error',
        'dest': 'processing_payment'},
    {'trigger': 'items_packed', 'source': 'processing_fulfillment',
        'dest': 'completed_shipped'},
    {'trigger': 'fulfillment_failed', 'source': 'processing_fulfillment',
        'dest': 'error_fulfillment_error'},
    {'trigger': 'retry_fulfillment', 'source': 'error_fulfillment_error',
        'dest': 'processing_fulfillment'},
    {'trigger': 'delivery_confirmed', 'source': 'completed_shipped',
        'dest': 'completed_delivered'},
    {'trigger': 'cancel_order', 'source': [
        'processing_validating', 'processing_payment', 'processing_fulfillment'], 'dest': 'cancelled'},
    {'trigger': 'cancel_order', 'source': [
        'completed_shipped'], 'dest': 'cancelled'},
    {'trigger': 'resolve_issue', 'source': 'error_validation_error', 'dest': 'idle'},
    {'trigger': 'resolve_issue', 'source': 'error_fulfillment_error',
        'dest': 'processing_fulfillment'},
    {'trigger': 'reset', 'source': [
        'error_validation_error', 'error_payment_error', 'error_fulfillment_error', 'cancelled', 'completed_delivered'], 'dest': 'idle'}
]

# Demo 2: User Authentication Flow
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
    {'trigger': 'credentials_valid', 'source': 'checking_credentials',
        'dest': 'mfa_required'},
    {'trigger': 'credentials_invalid', 'source': 'checking_credentials',
        'dest': 'logged_out'},
    {'trigger': 'too_many_attempts', 'source': 'checking_credentials',
        'dest': 'locked_out'},
    {'trigger': 'mfa_success', 'source': 'mfa_required', 'dest': 'authenticated'},
    {'trigger': 'mfa_fail', 'source': 'mfa_required', 'dest': 'logged_out'},
    {'trigger': 'logout', 'source': 'authenticated', 'dest': 'logged_out'},
    {'trigger': 'session_timeout', 'source': 'authenticated',
        'dest': 'session_expired'},
    {'trigger': 'relogin', 'source': 'session_expired',
        'dest': 'checking_credentials'},
    {'trigger': 'unlock', 'source': 'locked_out', 'dest': 'logged_out'}
]

# Demo 3: Document Workflow
document_states = [
    'draft',
    'in_review',
    'approved',
    'published',
    'archived',
    'rejected'
]

document_transitions = [
    {'trigger': 'submit_for_review', 'source': 'draft', 'dest': 'in_review'},
    {'trigger': 'approve', 'source': 'in_review', 'dest': 'approved'},
    {'trigger': 'reject', 'source': 'in_review', 'dest': 'rejected'},
    {'trigger': 'revise', 'source': 'rejected', 'dest': 'draft'},
    {'trigger': 'publish', 'source': 'approved', 'dest': 'published'},
    {'trigger': 'unpublish', 'source': 'published', 'dest': 'approved'},
    {'trigger': 'archive', 'source': [
        'approved', 'published'], 'dest': 'archived'},
    {'trigger': 'restore', 'source': 'archived', 'dest': 'draft'}
]

# Demo 4: Traffic Light (Simple)
traffic_states = ['red', 'yellow', 'green']

traffic_transitions = [
    {'trigger': 'next', 'source': 'red', 'dest': 'green'},
    {'trigger': 'next', 'source': 'green', 'dest': 'yellow'},
    {'trigger': 'next', 'source': 'yellow', 'dest': 'red'},
    {'trigger': 'emergency', 'source': ['green', 'yellow'], 'dest': 'red'}
]

# Demo 5: CI/CD Pipeline
cicd_states = [
    'idle',
    {
        'name': 'building',
        'children': ['compile', 'test', 'package']
    },
    {
        'name': 'deploying',
        'children': ['staging', 'production']
    },
    'deployed',
    {
        'name': 'failed',
        'children': ['build_failed', 'test_failed', 'deploy_failed']
    }
]

cicd_transitions = [
    {'trigger': 'start_build', 'source': 'idle', 'dest': 'building_compile'},
    {'trigger': 'compile_success', 'source': 'building_compile',
        'dest': 'building_test'},
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

# Create all machines
machines = {
    'order': ReactFlowMachine(states=order_states, transitions=order_transitions, initial='idle'),
    'auth': ReactFlowMachine(states=auth_states, transitions=auth_transitions, initial='logged_out'),
    'document': ReactFlowMachine(states=document_states, transitions=document_transitions, initial='draft'),
    'traffic': ReactFlowMachine(states=traffic_states, transitions=traffic_transitions, initial='red'),
    'cicd': ReactFlowMachine(states=cicd_states, transitions=cicd_transitions, initial='idle')
}

# Generate graph data for all machines
graph_data = {name: machine.get_graph() for name, machine in machines.items()}


@app.route('/graph-data')
def get_all_graph_data():
    """Serve all state machine graph data"""
    return jsonify(graph_data)


@app.route('/graph-data/<machine_name>')
def get_graph_data_by_name(machine_name):
    """Serve specific state machine graph data"""
    if machine_name in graph_data:
        return jsonify(graph_data[machine_name])
    return jsonify({'error': 'Machine not found'}), 404


@app.route('/')
def serve_index():
    """Serve the index.html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    print("Starting server at http://localhost:5050")
    print("\nAvailable state machines:")
    for name, data in graph_data.items():
        print(
            f"  - {name}: {len(data['nodes'])} nodes, {len(data['edges'])} edges")
    print("\nEndpoints:")
    print("  - http://localhost:5050/graph-data (all machines)")
    print("  - http://localhost:5050/graph-data/<machine_name> (specific machine)")
    app.run(debug=True, port=5050)
