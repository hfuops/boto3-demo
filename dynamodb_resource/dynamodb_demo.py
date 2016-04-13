#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/13 10:36
"""
使用dynamodb
"""

# 创建表
import boto3
from boto3.dynamodb.conditions import Key, Attr


def create_user_table(table_name='users'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(TableName=table_name,
                                  KeySchema=[
                                      {
                                          'AttributeName': 'username',
                                          'KeyType': 'HASH'
                                      }, {
                                          'AttributeName': 'last_name',
                                          'KeyType': 'RANGE'
                                      }
                                  ],
                                  AttributeDefinitions=[
                                      {
                                          'AttributeName': 'username',
                                          'AttributeType': 'S'
                                      }, {
                                          'AttributeName': 'last_name',
                                          'AttributeType': 'S'
                                      }
                                  ],
                                  ProvisionedThroughput={
                                      'ReadCapacityUnits': 5,
                                      'WriteCapacityUnits': 5
                                  })
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print table.item_count


# 获取已有表
def get_table(table_name='users'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    print table.creation_date_time


# 新增一条记录
def create_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    table.put_item(
        Item={
            "username": "wang xiaoming",
            "first_name": "xiaoming",
            "last_name": "wang",
            "age": 25,
            "account_type": "standard_user"
        }
    )

    print "created item!"


def get_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    response = table.get_item(
        Key={
            'username': 'wang xiaoming',
            'last_name': 'wang'
        }
    )

    return response['Item']


# 更新一条记录
def update_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    table.update_item(
        Key={
            'username': 'wang xiaoming',
            'last_name': 'wang'
        },
        UpdateExpression='SET age = :val1',
        ExpressionAttributeValues={
            ":val1": 26 + 5
        }
    )


def delete_item():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    response = table.delete_item(
        Key={
            'username': 'wang xiaoming',
            'last_name': 'wang'
        }
    )
    # {'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'FOGP8VEBEBCLAT350OQULK430BVV4KQNSO5AEMVJF66Q9ASUAAJG'}}
    # 可以多次执行, 如果没有对应的记录, 也不会报错
    return response


# 批量插入
def batch_create_items():
    data = [
        {
            'account_type': 'standard_user',
            'username': 'johndoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 25,
            'address': {
                'road': '1 Jefferson Street',
                'city': 'Los Angeles',
                'state': 'CA',
                'zipcode': 90001
            }
        }, {
            'account_type': 'super_user',
            'username': 'janedoering',
            'first_name': 'Jane',
            'last_name': 'Doering',
            'age': 40,
            'address': {
                'road': '2 Washington Avenue',
                'city': 'Seattle',
                'state': 'WA',
                'zipcode': 98109
            }
        }, {
            'account_type': 'standard_user',
            'username': 'bobsmith',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'age': 18,
            'address': {
                'road': '3 Madison Lane',
                'city': 'Louisville',
                'state': 'KY',
                'zipcode': 40213
            }
        }, {
            'account_type': 'super_user',
            'username': 'alicedoe',
            'first_name': 'Alice',
            'last_name': 'Doe',
            'age': 27,
            'address': {
                'road': '1 Jefferson Street',
                'city': 'Los Angeles',
                'state': 'CA',
                'zipcode': 90001
            }
        }
    ]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(Item=item)

    print "batch created items!"


# 条件查询
def query_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    response = table.query(
        KeyConditionExpression=Key('username').eq('johndoe')
    )

    return response['Items']


# 扫描表
def scan_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    response = table.scan(
        FilterExpression=Attr('age').lt(27)
    )

    return response['Items']


# 扫描表: 复合条件
def scan_complex_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    response = table.scan(
        FilterExpression=Attr('first_name').begins_with('J') & Attr('account_type').eq('super_user')
    )

    return response['Items']


# 扫描表: 属性嵌套查询: 使用.进行层次分割
def scan_nested_attr_query():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    response = table.scan(
        FilterExpression=Attr('address.state').eq('CA')
    )
    return response['Items']


# 删除表
def delete_table(table_name='users'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.delete()


if __name__ == '__main__':
    delete_table()
