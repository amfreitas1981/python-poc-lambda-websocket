import json
import boto3
import os

# API Gateway
dynamo_db = boto3.client('dynamodb')
table_name = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    print(f"User is connected with event {json.dumps(event)}")

    req_context = event["requestContext"]
    connection_id = req_context["connectionId"]

    params = event.get("queryStringParameters") or {}
    session_id = params.get("session")

    if not session_id:
        print("query param 'session' is required")
        return {
            'statusCode': 400
        }

    dynamo_db.put_item(
        TableName=table_name,
        Item={
            'session_id': {'S': session_id},
            'connection_id': {'S': connection_id}
        }
    )

    return {
        'statusCode': 200
    }
