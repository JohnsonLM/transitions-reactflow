import json
from transitions_reactflow.machine import ReactFlowMachine

states = [
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

transitions = [
    # From idle to processing substates
    {'trigger': 'start_order', 'source': 'idle', 'dest': 'processing_validating'},

    # Validation flow
    {'trigger': 'validation_pass', 'source': 'processing_validating',
        'dest': 'processing_payment'},
    {'trigger': 'validation_fail', 'source': 'processing_validating',
        'dest': 'error_validation_error'},

    # Payment flow
    {'trigger': 'payment_approved', 'source': 'processing_payment',
        'dest': 'processing_fulfillment'},
    {'trigger': 'payment_declined', 'source': 'processing_payment',
        'dest': 'error_payment_error'},
    {'trigger': 'payment_retry', 'source': 'error_payment_error',
        'dest': 'processing_payment'},

    # Fulfillment flow
    {'trigger': 'items_packed', 'source': 'processing_fulfillment',
        'dest': 'completed_shipped'},
    {'trigger': 'fulfillment_failed', 'source': 'processing_fulfillment',
        'dest': 'error_fulfillment_error'},
    {'trigger': 'retry_fulfillment', 'source': 'error_fulfillment_error',
        'dest': 'processing_fulfillment'},

    # Completed flow
    {'trigger': 'delivery_confirmed', 'source': 'completed_shipped',
        'dest': 'completed_delivered'},

    # Cancellation from various states
    {'trigger': 'cancel_order', 'source': [
        'processing_validating', 'processing_payment', 'processing_fulfillment'], 'dest': 'cancelled'},
    {'trigger': 'cancel_order', 'source': [
        'completed_shipped'], 'dest': 'cancelled'},

    # Recovery from errors
    {'trigger': 'resolve_issue', 'source': 'error_validation_error', 'dest': 'idle'},
    {'trigger': 'resolve_issue', 'source': 'error_fulfillment_error',
        'dest': 'processing_fulfillment'},

    # Reset from various terminal states
    {'trigger': 'reset', 'source': [
        'error', 'cancelled', 'completed_delivered'], 'dest': 'idle'}
]

machine = ReactFlowMachine(
    states=states, transitions=transitions, initial='idle')

# Generate the React Flow JSON
graph_data = machine.get_graph()

print(json.dumps(graph_data, indent=2))
