import json
import parameter

from libs.home_class import HomeClass

VALID_PARAMS = [
    's_d',
    't'
]

def lambda_handler(event, context):

    db_params = parameter.get()

    request_params = {}
    for p in VALID_PARAMS:
        if p in event.get('queryStringParameters', {}).keys():
            request_params[p] = event['queryStringParameters'][p]

    home_cls        = HomeClass(db_params)
    home_cls.params = request_params
    home_cls.build()

    return {
        'statusCode': home_cls.status_code,
        'body': json.dumps({
            'response': home_cls.response['result']
        })
    }
