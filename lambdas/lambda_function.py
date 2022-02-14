import boto3
import json



# ------- Skill specific business logic -------

SKILL_NAME = "ECE IOT Framework"

# Make sure you use question marks or periods.

def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest, etc).
    The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    print("event:" + json.dumps(event))

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """Called when the session starts."""
    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """Called when the user launches the skill without specifying what they want."""
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill."""
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    print("***********************intent section***************************")
    print(intent_name)
    if intent_name == "TimInt":
        return handle_timintent_request(intent, session)
    elif intent_name == "MichaelInt":
        return handle_michaelintent_request(intent, session)
    elif intent_name == "DanielInt":
        return handle_danielintent_request(intent, session)
    elif intent_name == "JanInt":
        return handle_janintent_request(intent, session)
    elif intent_name == "MarkusInt":
        return handle_markusintent_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior -------------


def get_welcome_response():
    """If we wanted to initialize the session to have some attributes we could add those here."""
    intro = ("Welcome to our ECE IOT project. With this Alexa Skill you can check your current sensor values. Tell me the desired device and sensor type ")
    should_end_session = False

    speech_output = intro
    reprompt_text = intro
    attributes = {"speech_output": speech_output,
                  "reprompt_text": speech_output
                  }

    return build_response(attributes, build_speechlet_response(
        SKILL_NAME, speech_output, reprompt_text, should_end_session))



def handle_timintent_request(intent, session):
    attributes = {}

    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("Sadly you don't have any fancy titles, quite unfortunate.")
    reprompt_text = "Don't you want to know who you really are, just ask {}".format(SKILL_NAME)

    sensor_result = sensor((intent['slots']['tim_sensortype']['value']), ("esp32_tim"), ("Lab 124"))
    sensor_result_unit = sensor_unit((intent['slots']['tim_sensortype']['value']), ("esp32_tim"), ("Lab 124"))
    speech_output=("The result of the sensor query is {:0.2f} {} in Lab 124".format(sensor_result, sensor_result_unit))
    print(speech_output)
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))

def handle_michaelintent_request(intent, session):
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("Sadly you don't have any fancy titles, quite unfortunate.")
    reprompt_text = "Don't you want to know who you really are, just ask {}".format(SKILL_NAME)

    sensor_result = sensor((intent['slots']['michael_sensortype']['value']), ("esp32_michael"), ("Lab 125"))
    sensor_result_unit = sensor_unit((intent['slots']['michael_sensortype']['value']), ("esp32_michael"), ("Lab 125"))
    speech_output=("The result of the sensor query is {:0.2f} {} in Lab 125".format(sensor_result, sensor_result_unit))
    print(speech_output)
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))

def handle_janintent_request(intent, session):
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("Sadly you don't have any fancy titles, quite unfortunate.")
    reprompt_text = "Don't you want to know all about your sensors, just ask {}".format(SKILL_NAME)

    sensor_result = sensor((intent['slots']['jan_sensortype']['value']), ("esp32_jan"), ("Lab 125"))
    sensor_result_unit = sensor_unit((intent['slots']['jan_sensortype']['value']), ("esp32_jan"), ("Lab 125"))
    speech_output=("The result of the sensor query is {:0.2f} {} in Lab 125".format(sensor_result, sensor_result_unit))
    print(speech_output)
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))

def handle_danielintent_request(intent, session):
    attributes = {}
    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("Sadly you don't have any fancy titles, quite unfortunate.")
    reprompt_text = "Don't you want to know who you really are, just ask {}".format(SKILL_NAME)

    sensor_result = sensor((intent['slots']['daniel_sensortype']['value']), ("esp32_daniel"), ("Lab 124"))
    sensor_result_unit = sensor_unit((intent['slots']['daniel_sensortype']['value']), ("esp32_daniel"), ("Lab 124"))
    speech_output=("The result of the sensor query is {:0.2f} {} in Lab 124".format(sensor_result, sensor_result_unit))
    print(speech_output)
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))


def handle_markusintent_request(intent, session):
    attributes = {}

    should_end_session = False
    user_gave_up = intent['name']
    speech_output = ("Sadly you don't have any fancy titles, quite unfortunate.")
    reprompt_text = "Don't you want to know who you really are, just ask {}".format(SKILL_NAME)

    sensor_result = sensor((intent['slots']['markus_sensortype']['value']), ("esp32_markus"), ("Lab 124"))
    sensor_result_unit = sensor_unit((intent['slots']['markus_sensortype']['value']), ("esp32_markus"), ("Lab 124"))
    speech_output=("The result of the sensor query is {:0.2f} {} in Lab 124".format(sensor_result, sensor_result_unit))
    print(speech_output)
    return build_response(
            {},
            build_speechlet_response(
                SKILL_NAME, speech_output, reprompt_text, should_end_session
            ))


def handle_get_help_request(intent, session):
    attributes = {}
    speech_output = "Just ask {} about your controller and sensors!".format(SKILL_NAME)
    reprompt_text = "what can I help you with?"
    should_end_session = False
    return build_response(
        attributes,
        build_speechlet_response(SKILL_NAME, speech_output, reprompt_text, should_end_session)
    )


def handle_finish_session_request(intent, session):
    """End the session with a message if the user wants to quit the app."""
    #attributes = session['attributes']
    attributes=""
    reprompt_text = None
    speech_output = "Thanks for using {}. Have a Great Day.".format(SKILL_NAME)
    should_end_session = True
    return build_response(
        attributes,
        build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)
    )

# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }

def sensor(type, device, room):
    timestream = boto3.client('timestream-query')
    location = room
    database_name = "measurement_fleet"
    table_name = device
    sensor = type
    QUERY = \
    "SELECT * " \
    "FROM " + database_name + "." + table_name +" " \
    "WHERE SensorType='"+sensor+"' and Location='"+location+"' " \
    "ORDER BY time DESC " \
    "LIMIT 1"
    response = timestream.query(QueryString=QUERY)
    result = float(response['Rows'][0]['Data'][3]['ScalarValue'])
    return result

def sensor_unit(type, device, room):
    timestream = boto3.client('timestream-query')
    location = room
    database_name = "measurement_fleet"
    table_name = device
    sensor = type
    QUERY = \
    "SELECT * " \
    "FROM " + database_name + "." + table_name +" " \
    "WHERE SensorType='"+sensor+"' and Location='"+location+"' " \
    "ORDER BY time DESC " \
    "LIMIT 1"
    response = timestream.query(QueryString=QUERY)
    result = str(response['Rows'][0]['Data'][5]['ScalarValue'])

    if result == "hPa":
        return "hectopascal"
    elif result =="ppm":
        return "parts per million"
    elif result == "lx":
        return "lux"
    else:
        return   result
