import logging


logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    logging.info(f'slots for intent {intent} => {slots}')

    if event['invocationSource'] == 'DialogCodeHook':
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Delegate',
                },
                'intent': {
                    'name': intent,
                    'slots': slots,
                },
            },
        }

    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Close',
            },
            'intent': {
                'name': intent,
                'slots': slots,
                'state': 'Fulfilled',
            },
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'Its over'
            }
        ]
    }

