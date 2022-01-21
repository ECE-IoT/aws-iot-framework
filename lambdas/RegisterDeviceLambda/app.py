from tokenize import String
import boto3
import os
import json
from boto3.dynamodb.conditions import Attr

DYNAMO_DB = 'dynamodb'
TIMESTREAM = 'timestream'
ATTR_ESP_MAC = 'ESP_MAC'
ATTR_ESP_ID = 'ESP_ID'


def lambda_handler(message, context):

    mac_adress = String
    device_name = String
    sensor_type = String

    if message:
        mac_adress = message["MAC_ADRESS"]
        device_name = message["DEVICE_NAME"]
        sensor_type = message["SENSOR_TYPE"]
    else:
        print("ERROR: no valid json object")
        return

    region = os.environ.get('Region', 'eu-central-1')
    dynamo_table_name = os.environ.get('DynamoDBTable', 'TopicTable')
    timestream_table_name = os.environ.get('TimestreamTable', 'DataTable')

    if region == "eu-central-1":
        dynamo = boto3.resource(DYNAMO_DB, region_name=region)
    else:
        print(f"ERROR could not fetch table at reagion {region}")
        pass

    dynamo_db = dynamo.Table(dynamo_table_name)

    if dynamo_db.scan(FilterExpression=Attr(ATTR_ESP_ID).contains(device_name)):
        print(f"LOG: device named {device_name} already exists")
        return
    else:
        print(
            f"LOG: device named {device_name} does not exists, creating new entry")
        params = {
            'ESP_MAC': mac_adress,
            'ESP_ID': device_name
        }
        response = dynamo_db.put_item(
            TableName=dynamo_table_name,
            Item=params
        )
        print(f"LOG: entry with the following message created: {response}")
