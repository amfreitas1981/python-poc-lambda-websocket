import json
import boto3
import os

# API Gateway
dynamo_db = boto3.client('dynamodb')
table_name = os.environ.get("TABLE_NAME")

def lambda_handler(event, context):
    print(f"User disconnected with event {json.dumps(event)}")

    req_context = event["requestContext"]
    connection_id = req_context["connectionId"]

    query_result = dynamo_db.query(
        TableName=table_name,
        IndexName='connection_id-index',
        ExpressionAttributeValues={':connection_id': {'S': connection_id}},
        KeyConditionExpression='connection_id = :connection_id'
    )

    if not query_result["Items"]:
        return {
            'statusCode': 404
        }

    session_id = query_result["Items"][0]["session_id"]["S"]
    dynamo_db.delete_item(
        TableName=table_name,
        Key={'session_id': {'S': session_id}}
    )

    return {
        'statusCode': 200
    }
