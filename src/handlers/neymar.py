import logging


logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    response = {
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
    logging.info(f'slots for intent {intent} => {slots}')

    if event['invocationSource'] == 'DialogCodeHook':
        return response

    if slots.get('ProblemCatalog') and slots['ProblemCatalog']['value']['originalValue'] == 'Ações':
        response['sessionState']['dialogAction']['type'] = 'Close'
        response['sessionState']['messages'] = [
            {
                'contentType': 'PlainText',
                'content': 'Certo, aqui está uma lista de ações para prosseguir com o problema:\n- Informar o codigo do erro para mais detalhes: basta digitar "Erro:" em seguida o codigo\n - Registrar um ticket para atendimento: se quiser saber como fazer, basta digitar "Abrir Ticket"'
            }
        ]
        response['sessionState']['intent']['state'] = 'Fulfilled'
    return response

