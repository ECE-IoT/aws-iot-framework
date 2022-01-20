# Response messages
WELCOME_MESSAGE = "Hi, welcome to our IOT Framework, you can ask me about your the actual value of your sensors!"
HELP_MESSAGE = "You can ask me about a specific value?"
HELP_REPROMPT = "What can I help you with?"
FALLBACK_MESSAGE = "I can't help you with that. It can tell you about your Framework",
FALLBACK_REPROMPT = "What can I help you with"
ERROR_MESSAGE = "Sorry, an error occurred."
STOP_MESSAGE = "Ok Bye"


# Provides senor details
def get_sensor_info(sensor_id):
    sensor = sensor_id.lower().replace('-', '').replace(' ', '')
    if sensor == '1':
        return ''
    elif sensor == '2':
        return ''
    elif sensor == '3':
        return ''
    elif sensor == '4':
        return ''
    elif sensor == '5':
        return ' '
    else:
        return 'No data found'
