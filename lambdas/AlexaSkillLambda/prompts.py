import boto3
from boto3.dynamodb.conditions import Key
import os

# Response messages
WELCOME_MESSAGE = "Hi, welcome to our IOT Framework, you can ask me about your the actual value of your sensors!"
HELP_MESSAGE = "You can ask me about a specific value?"
HELP_REPROMPT = "What can I help you with?"
FALLBACK_MESSAGE = "I can't help you with that. It can tell you about your Framework",
FALLBACK_REPROMPT = "What can I help you with"
ERROR_MESSAGE = "Sorry, an error occurred."
STOP_MESSAGE = "Ok Bye"

# Query specific constants
DYNAMO_DB = 'dynamodb'
DYN_DYB_TABLE = "TopicTable"
TIMESTREAM_DB = "measurement_fleet"
ATTR_ESP_MAC = 'ESP_MAC'
ATTR_ESP_ID = 'ESP_ID'


def response(sensor_type, position):
    if sensor_type:
        fetch_sensor_response(sensor_type, position)


def fetch_sensor_response(sensor_type, position):
    measured_object = get_sensor_value(sensor_type, position)
    value = float()

    for val in measured_object:
        value = value + round(float(val['Value']))

    value = value / len(measured_object)
    name = measured_object[0]['SensorType']
    unit = measured_object[0]['Unit']
    position = measured_object[0]['Location']

    print(f"The {name} is {value} {unit} in {position}")


def get_sensor_value(sensor_type, position):
    timestream_client = boto3.client('timestream-query')

    region = os.environ.get('Region', 'eu-central-1')

    if region == "eu-central-1":
        dynamodb_table = boto3.resource(DYNAMO_DB, region_name=region)
    else:
        return ERROR_MESSAGE

    dynamo = dynamodb_table.Table(DYN_DYB_TABLE)
    filtered_dynamodb = dynamo.scan()['Items']
    devices = list()
    query_response = list()

    for items in filtered_dynamodb:
        devices.append(items[ATTR_ESP_ID])

    for device in devices:
        data_value = list()
        column_list = list()
        query = f"SELECT * FROM {TIMESTREAM_DB}.{device} WHERE SensorType = '{sensor_type}' AND Location = '{position}' LIMIT 1"
        result = timestream_client.query(QueryString=query)

        data = result['Rows'][0]['Data']
        for d in data:
            data_value.append(d['ScalarValue'])

        column_info = result['ColumnInfo']
        for col in column_info:
            column_list.append(col['Name'])

        query_response.append(convert_to_dict(column_list, data_value))

    return query_response


def convert_to_dict(key_list, value_list):
    return {key_list[i]: value_list[i] for i in range(len(key_list))}
