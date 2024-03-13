import json
import boto3
import os
import logging
from uuid import uuid4


logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    bot_id = os.environ.get('BOT_ID', '')
    bot_alias_id = os.environ.get('BOT_ALIAS_ID', '').split('|')[0] # a referencia do alias retorna isso: alias_id|bot_id

    logging.info(f'event -> {event}')

    body = json.loads(event.get('body', ''))
    user_message = body.get('message', '')

    logging.info(f'sending the message {user_message} to the bot {bot_id} with alis {bot_alias_id}')

    lex_runtime = boto3.client('lexv2-runtime')
    lex_response = lex_runtime.recognize_text(
        botId=bot_id,
        botAliasId=bot_alias_id,
        localeId='pt_BR',
        sessionId=str(uuid4()),
        text=user_message,
    )

    response = lex_response

    logging.info(response)

    return {
        'statusCode': 200,
        'body': json.dumps(response.get('messages')),
        'isBase64Encoded': False,
        "headers": {
            "Content-Type": "application/json"
        },
    }

