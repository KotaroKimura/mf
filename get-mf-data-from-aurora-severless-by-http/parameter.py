import boto3

def get():

    ssm          = boto3.client('ssm')
    ssm_response = ssm.get_parameters(
        Names = [
            'mf-db-cluster-arn',
            'mf-db-credentials-secrets-store-arn'
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
