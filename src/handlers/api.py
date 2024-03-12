import json
import boto3
import os
from uuid import uuid4


def lambda_handler(event, context):
    bot_id = os.environ.get('BOT_ID', '')
    bot_alias_id = os.environ.get('BOT_ALIAS_ID', '').split('|')[0] # a referencia do alias retorna isso: alias_id|bot_id

    body = json.loads(event.get('body', ''))
    user_message = body.get('message', '')

    lex_runtime = boto3.client('lexv2-runtime')
    lex_response = lex_runtime.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        localeId='pt_BR',
        sessionId=str(uuid4()),
        text=user_message,
    )

    response = json.dumps(lex_response)

    return {
        'statusCode': 200,
        'body': response,
        'isBase64Encoded': False,
        "headers": {
            "Content-Type": "application/json"
        },
    }

