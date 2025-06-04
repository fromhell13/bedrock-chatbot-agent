
import json

def extract_customer_data(event):
    # Extracting the properties list
    properties = event['requestBody']['content']['application/json']['properties']
    customer_data = {prop['name']: prop['value'] for prop in properties if prop['name'] in ['customerName', 'customerEmail', 'complaintType', 'customerPhone']}
    print(f"customer_data: {customer_data}")
    return customer_data
def send_complaint(parameters):
    return parameters

def lambda_handler(event, context):
    responses = []

    print(f"event here: {event}")
    print(f"requestBody: {event.get('requestBody')}")

    api_path = event['apiPath']

    if api_path == '/send-complaint':
        parameters = extract_customer_data(event)
        body = send_complaint(parameters)
                
    # prepare response
    response_body = {
        'application/json': {
            'body': json.dumps(body)
        }
    }
        
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        "sessionId": event['sessionId'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }

    responses.append(action_response)
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response}
        
    return api_response
