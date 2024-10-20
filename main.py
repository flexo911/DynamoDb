import boto3
from flask import Flask, jsonify

# Підключення до DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-west-2',
    endpoint_url='http://dynamodb-local:8000',
    aws_access_key_id='local',
    aws_secret_access_key='local'

)

def table_exists(table_name: str) -> bool:
    try:
        dynamodb.Table(table_name).table_status
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        return False
    return True

def create_db_table():
    if  table_exists('ExampleTable') :
        return '{message:"table isset"}'
    else:
        table = dynamodb.create_table(
            TableName='ExampleTable',
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'SortKey',
                    'KeyType': 'RANGE'  # Sort key (не обов'язковий)
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'SortKey',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Чекаємо, поки таблиця не буде готова
        table.meta.client.get_waiter('table_exists').wait(TableName='ExampleTable')
        return '{message:"Таблиця створена успішно"}'

def get_db_items():
    table = dynamodb.Table('ExampleTable')
    response = table.scan()
    items = response.get('Items', [])
    return jsonify(items)

def edit_db_item():
    table = dynamodb.Table('ExampleTable')
    response = table.update_item(
        Key={
            'ID': 1,
            'SortKey': 'A'
        },
        UpdateExpression="set Age = :age, IsActive = :status",
        ExpressionAttributeValues={
            ':age': 31,
            ':status': False
        },
        ReturnValues="UPDATED_NEW"
    )
    return {'message':"Edited", 'response': response }



def add_db_item():
    table = dynamodb.Table('ExampleTable')

    new_item = {
        'ID': 6,
        'SortKey': 'F',
        'Name': 'Diana Blue',
        'Age': 22,
        'IsActive': True,
        'Tags': ['QA', 'Test Automation'],
        'Metadata': {'Role': 'User', 'Location': 'IN'}
    }

    table.put_item(Item=new_item)

    return '{message:"Новий запис додано"}'


def add_db_items():
    table = dynamodb.Table('ExampleTable')

    items = [
        {
            'ID': 1,
            'SortKey': 'A',
            'Name': 'John Doe',
            'Age': 30,
            'IsActive': True,
            'Tags': ['Developer', 'Python'],
            'Metadata': {'Role': 'Admin', 'Location': 'US'}
        },
        {
            'ID': 2,
            'SortKey': 'B',
            'Name': 'Jane Smith',
            'Age': 25,
            'IsActive': False,
            'Tags': ['Manager'],
            'Metadata': {'Role': 'User', 'Location': 'UK'}
        },
        {
            'ID': 3,
            'SortKey': 'C',
            'Name': 'Alice Brown',
            'Age': 35,
            'IsActive': True,
            'Tags': ['Engineer', 'AWS'],
            'Metadata': {'Role': 'Admin', 'Location': 'CA'}
        },
        {
            'ID': 4,
            'SortKey': 'D',
            'Name': 'Bob White',
            'Age': 40,
            'IsActive': False,
            'Tags': ['HR'],
            'Metadata': {'Role': 'User', 'Location': 'AU'}
        },
        {
            'ID': 5,
            'SortKey': 'E',
            'Name': 'Chris Green',
            'Age': 28,
            'IsActive': True,
            'Tags': ['DevOps', 'Docker'],
            'Metadata': {'Role': 'Admin', 'Location': 'DE'}
        }
    ]

    for item in items:
        table.put_item(Item=item)
    return '{message:"Дані додані успішно."}'

def get_db_sorted_items():
    table = dynamodb.Table('ExampleTable')
    response = table.get_item(
        Key={
            'ID': 1,
            'SortKey': 'A'
        }
    )
    return {'message':"Отриманий запис.", 'data':response}

def get_db_scan_table():
    table = dynamodb.Table('ExampleTable')
    response = table.scan()
    return {'message':"Отриманий запис.", 'data':response}


def get_db_filtered_table():
    table = dynamodb.Table('ExampleTable')
    response = table.scan(
        FilterExpression="IsActive = :active_status",
        ExpressionAttributeValues={':active_status': True}
    )
    return {'message':"Отриманий запис.", 'data':response}
