from threading import local
from tokenize import String
from urllib import response
import boto3
import os
import json
from boto3.dynamodb.conditions import Attr, Key

DYNAMO_DB = 'dynamodb'
TIMESTREAM = 'timestream'
TS_TABLE_NAME = "measurement_fleet"
ATTR_ESP_MAC = 'ESP_MAC'
ATTR_ESP_ID = 'ESP_ID'


def lambda_handler(message, context):

    mac_adress = String
    device_name = String

    if message:
        mac_adress = message["MAC_ADRESS"]
        device_name = message["DEVICE_NAME"]
    else:
        print("ERROR: no valid json object")
        return

    region = os.environ.get('Region', 'eu-central-1')
    dynamo_table_name = os.environ.get('DynamoDBTable', 'TopicTable')

    if region == "eu-central-1":
        dynamo = boto3.resource(DYNAMO_DB, region_name=region)
    else:
        print(f"ERROR could not fetch table at reagion {region}")
        pass

    dynamo_db = dynamo.Table(dynamo_table_name)
    timestream_client = boto3.client('timestream-write')

    r = dynamo_db.scan()
    print(r)

    filtered_items = dynamo_db.query(
        KeyConditionExpression=Key(ATTR_ESP_MAC).eq(mac_adress))['Items']

    if filtered_items:
        for f in filtered_items:
            device = f[ATTR_ESP_ID]
            if device == device_name:
                print(f"LOG: device named {device} already exists")
                return

    print(
        f"LOG: device named {device_name} does not exists, creating new entry")
    params = {
        'ESP_MAC': mac_adress,
        'ESP_ID': device_name
    }
    dynamo_db.put_item(
        TableName=dynamo_table_name,
        Item=params
    )
    print(f"LOG: DynamoDB entry created")
    print(
        f"LOG: creating new Table for Timestream database: {TS_TABLE_NAME}")

    print(TS_TABLE_NAME)

    timestream_tables = timestream_client.list_tables(
        DatabaseName=TS_TABLE_NAME)

    print(timestream_tables)
