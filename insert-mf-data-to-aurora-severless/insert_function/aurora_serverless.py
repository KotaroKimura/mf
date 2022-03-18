import boto3
rds_client = boto3.client('rds-data')

def execute(db_cluster_arn, db_credentials_secrets_store_arn, sql):

    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_store_arn,
        database='mf',
        resourceArn=db_cluster_arn,
        sql=sql
    )

    return response

def bad_request_exception_class():
    return rds_client.exceptions.BadRequestException
