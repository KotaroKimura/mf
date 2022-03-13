import boto3

def get(event):

    param_1 = ''
    param_2 = ''
    param_3 = ''
    param_4 = ''
    try:
        param_1 = event['param_1']
        param_2 = event['param_2']
        param_3 = event['param_3']
        param_4 = event['param_4']
    except KeyError as e:
        return {
            "error": "param_exists_error",
            "param_name": str(e).replace("'", '')
        }

    ssm          = boto3.client('ssm')
    ssm_response = ssm.get_parameters(
        Names = [
            param_1,
            param_2,
            param_3,
            param_4
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
