# lambda/index.py（修正版）
import json
import os
import urllib.request

FASTAPI_URL = os.environ.get("FASTAPI_URL", "https://your-colab-url.ngrok.io/generate")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        message = body["message"]
        conversation_history = body.get("conversationHistory", [])

        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            FASTAPI_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read().decode("utf-8"))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }