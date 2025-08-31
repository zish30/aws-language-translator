import json
import boto3

translate = boto3.client("translate")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        text = body.get("text")
        target_lang = body.get("target_lang")

        if not text or not target_lang:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Missing 'text' or 'target_lang'"})
            }

        # Auto-detect source language and translate
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_lang
        )

        translated_text = response["TranslatedText"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"translated_text": translated_text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
