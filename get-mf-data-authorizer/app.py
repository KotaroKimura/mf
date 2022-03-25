import json
import boto3
import base64

def get_basic_secrets(event):

    ssm          = boto3.client('ssm')
    ssm_response = ssm.get_parameters(
        Names = [
            'mf-api-basic-user',
            'mf-api-basic-password'
        ],
        WithDecryption = True
    )

    params = {}
    for param in ssm_response['Parameters']:
        params[param['Name']] = param['Value']

    if len(ssm_response['InvalidParameters']) > 0:
        return {
            "error": "param_name_error",
            "param_name": ', '.join(ssm_response['InvalidParameters'])
        }

    return params

def lambda_handler(event, context):
    secrets  = get_basic_secrets(event)
    user_id  = secrets['mf-api-basic-user']
    password = secrets['mf-api-basic-password']

    auth_str = 'Basic ' + base64.b64encode(f"{user_id}:{password}".encode("utf-8")).decode("ascii")

    auth_header = event['headers']['authorization']

    if auth_str != auth_header:
        raise Exception('Unauthorized')

    return {
        'principalId': user_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': event['routeArn']
                }
            ]
        }
    }
