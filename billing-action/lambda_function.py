
import json

accounts = [
  {
    "customer_name": "John Doe",
    "account_name": "1234",
    "account_status": "working",
    "total amount due": "RM0.00"
  },
  {
    "customer_name": "Jane Smith",
    "account_name": "5678",
    "account_status": "overdue",
    "total amount due": "RM29.00"
  },
  {
    "customer_name": "Alice Johnson",
    "account_name": "9012",
    "account_status": "terminated",
    "total amount due": "RM0.00"
  },
  {
    "customer_name": "Bob Williams",
    "account_name": "3456",
    "account_status": "working",
    "total amount due": "RM0.00"
  }
]

def filter_customer_account(accountNum):
    account_name_to_filter = accountNum
    filtered_account = [account for account in accounts if account["account_name"] == account_name_to_filter]
    return filtered_account

def generate_payment_link(accountNum):

    return f"https://paymentgateway.com/pay?accountId={accountNum}"

def lambda_handler(event, context):
    responses = []

    print(f"event here: {event}")
    print(f"parameters: {event.get('parameters')}")

    api_path = event['apiPath']

    if api_path == '/check-account/{accountNum}': #check customer account
        parameters = event['parameters']
        for parameter in parameters:
            if parameter["name"] == "accountNum":
                accountNum = parameter["value"]

            body = filter_customer_account(accountNum)
    elif api_path == '/generate-payment-link/{accountNum}':
        parameters = event['parameters']
        for parameter in parameters:
            if parameter["name"] == "accountNum":
                accountNum = parameter["value"]
        body = generate_payment_link(accountNum)
                
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
