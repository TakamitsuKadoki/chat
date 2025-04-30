import json
import requests
import os

FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://your-colab-url.ngrok.io/generate")

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])

        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        print("Sending request to FastAPI:", FASTAPI_URL)
        res = requests.post(FASTAPI_URL, json=payload)
        res.raise_for_status()
        result = res.json()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }