import json
import boto3
import os

# Sei que não é o Dynamo que será utilizado. Vou verificar qual será aplicado para substituir
# API Gateway

endpoint_url = os.environ.get("WS_ENDPOINT")
table_name = os.environ.get("TABLE_NAME")

api_gateway_mngmt = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
dynamo_db = boto3.client('dynamodb')

def lambda_handler(event, context):
    json_body = event.get("body")
    body = json.loads(json_body)

    sessions = body.get("sessions", [])
    if not sessions:
        return {
            'statusCode': 400, 'body': 'No sessions provided'
        }

    session_key_list = [{"session_id": {"S": session}} for session in sessions]

    response = dynamo_db.batch_get_item(
        RequestItems={table_name: {'Keys': session_key_list}}
    )

    res_objects = response["Responses"][table_name]
    del body["sessions"]

    for res in res_objects:
        connection_id = res["connection_id"]["S"]
        api_gateway_mngmt.post_to_connection(
            Data=json.dumps(body).encode("utf-8"),
            ConnectionId=connection_id
        )

    return {
        'statusCode': 200
    }
