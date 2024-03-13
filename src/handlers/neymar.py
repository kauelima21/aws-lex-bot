import logging


logging.getLogger().setLevel(logging.INFO)


def problem_intent(interpreted_value: str, response: dict):
    interpreted_values_list = ['Ações', 'Visualizar recursos']

    if interpreted_value not in interpreted_values_list:
        return response

    response['sessionState']['dialogAction']['type'] = 'Close'
    response['sessionState']['intent']['state'] = 'Fulfilled'

    if interpreted_value == interpreted_values_list[0]:
        fulfill_response = {
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Certo, aqui está uma lista de ações para prosseguir com o problema:\n- Informar o codigo do erro para mais detalhes: basta digitar "Erro:" em seguida o codigo\n- Registrar um ticket para atendimento: se quiser saber como fazer, basta digitar "Abrir Ticket"'
                },
            ]
        }
        response.update(fulfill_response)
    if interpreted_value == interpreted_values_list[1]:
        fulfill_response = {
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Certo, aqui está uma lista de ações para prosseguir com o problema:\n- Registrar um ticket para atendimento: se quiser saber como fazer, basta digitar "Abrir Ticket"'
                },
            ]
        }
        response.update(fulfill_response)

    return response


def doubt_intent(interpreted_value: str, response: dict):
    interpreted_values_list = ['Como utilizar um recurso']

    if interpreted_value not in interpreted_values_list:
        return response

    response['sessionState']['dialogAction']['type'] = 'Close'
    response['sessionState']['intent']['state'] = 'Fulfilled'

    if interpreted_value == interpreted_values_list[0]:
        fulfill_response = {
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': 'Certo, aqui está uma lista de ações para prosseguir com a sua dúvida:\n- Registrar um ticket para atendimento: se quiser saber como fazer, basta digitar "Abrir Ticket"'
                },
            ]
        }
        response.update(fulfill_response)

    return response


def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    logging.info(f'slots for intent {intent} => {slots}')

    invocation_source = event['invocationSource']
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

    logging.info(f'invocationSource => {invocation_source}')

    if invocation_source == 'DialogCodeHook':
        return response

    interpreted_value = ''
    if slots.get('ProblemCatalog', None):
        interpreted_value = slots['ProblemCatalog']['value']['interpretedValue']
        response = problem_intent(interpreted_value, response)

    if slots.get('DoubtCatalog', None):
        interpreted_value = slots['DoubtCatalog']['value']['interpretedValue']
        response = doubt_intent(interpreted_value, response)

    logging.info(response)
    return response

