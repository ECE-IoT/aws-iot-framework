from tokenize import String
import boto3
import os
from boto3.dynamodb.conditions import Key

DYNAMO_DB = 'dynamodb'
TIMESTREAM = 'timestream'
TIMESTEAM_ROLE = 'TimestreamRole'
IOT_ROLE = "IoTRole"
TS_DB_NAME = "measurement_fleet"
ATTR_ESP_MAC = 'ESP_MAC'
ATTR_ESP_ID = 'ESP_ID'


def lambda_handler(message, context):

    mac_adress = String
    device_name = String
    role_arn = String

    if message:
        mac_adress = message["MAC_ADRESS"]
        device_name = message["DEVICE_NAME"]
    else:
        print("ERROR: no valid json object")
        return

    region = os.environ.get('Region', 'eu-central-1')
    dynamo_table_name = os.environ.get('DynamoDBTable', 'TopicTable')
    iam_client = boto3.client('iam')
    iot_client = boto3.client('iot')
    timestream_role = iam_client.get_role(RoleName=IOT_ROLE)['Role']
    iot_sql_topic = f"SELECT VALUE FROM '{device_name}/#'"

    if timestream_role:
        role_arn = timestream_role['Arn']
        print(f"LOG: fetching role ARN: {role_arn}")
    else:
        print("ERROR: Role permissions could not be fetched")
        return

    if region == "eu-central-1":
        dynamo = boto3.resource(DYNAMO_DB, region_name=region)
    else:
        print(f"ERROR could not fetch table at region {region}")
        return

    dynamo_db = dynamo.Table(dynamo_table_name)
    timestream_client = boto3.client('timestream-write')

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
        f"LOG: creating new Table for Timestream database: {TS_DB_NAME}")

    timestream_tables = timestream_client.list_tables(
        DatabaseName=TS_DB_NAME)['Tables']

    if timestream_tables:
        for t in timestream_tables:
            table = t['TableName']
            if table == device_name:
                print(f"ERROR: table already exists!")
                return

    timestream_client.create_table(DatabaseName=TS_DB_NAME, TableName=device_name, RetentionProperties={
        'MemoryStoreRetentionPeriodInHours': 6,
        'MagneticStoreRetentionPeriodInDays': 180
    }, MagneticStoreWriteProperties={
        'EnableMagneticStoreWrites': True})

    new_iot_rule = iot_client.create_topic_rule(ruleName=device_name, topicRulePayload={
        'sql': iot_sql_topic,
        'description': "IoT Rule for Device",
        'actions': [
            {'timestream': {
                'roleArn': role_arn,
                'databaseName': TS_DB_NAME,
                'tableName': device_name,
                'dimensions': [
                    {
                        'name': 'ID',
                        'value': '${MAC_ADRESS}'
                    },
                    {
                        'name': 'Name',
                        'value': '${DEVICE_NAME}'
                    },
                    {
                        'name': 'SensorType',
                        'value': '${SENSOR_TYPE}'
                    },
                    {
                        'name': 'SensorID',
                        'value': '${UNIQUE_SENSOR_ID}'
                    },
                    {
                        'name': 'Value',
                        'value': '${VALUE}'
                    },
                    {
                        'name': 'Unit',
                        'value': '${UNIT}'
                    },
                    {
                        'name': 'MeasurementTime',
                        'value': '${TIME}'
                    },
                ],
                'timestamp': {
                    'value': '${TIME}',
                    'unit': 'SECONDS'
                }
            }
            }
        ],
        'ruleDisabled': False,
    })

    print(f"LOG: new Rule created, log message: {new_iot_rule}")
