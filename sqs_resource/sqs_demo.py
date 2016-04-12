#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 11:17

import boto3

"""
SQS 是亚马逊的消息队列服务
基本操作:
    创建队列
    获取队列
    将消息发送到指定队列
    消费消息
"""


def sqs_create_queue(queue_name, attributes={}):
    attributes = attributes if attributes else {"DelaySeconds": "5"}

    sqs = boto3.resource('sqs')
    sqs.create_queue(QueueName=queue_name, Attributes=attributes)


def sqs_get_queue(queue_name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    # queue.url
    # queue.attributes.get('DelaySeconds')
    # get queue name from queue object
    # queue.attributes['QueueArn'].split(':')[-1]
    return queue


def sqs_get_queue_by_url(url):
    sqs = boto3.resource('sqs')

    # 等同于: sqs.Queue(url)
    return sqs.Queue(url=url)


def sqs_get_all_queues():
    return boto3.resource('sqs').queues.all()


def sqs_send_message(queue_name, message, attributes={}):
    """

    :param queue_name:
    :param message:
    :param attributes: 附带的元数据描述, 例如:
    {
        'Author': {
            'StringValue':'SKYFREE',
            'DataType':'String'
        }
    }
    :return:
    """
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    # 发送消息
    response = queue.send_message(MessageBody=message, MessageAttributes=attributes)

    # response.get('MessageId')
    # response.get('MD5OfMessageBody')
    return response


def sqs_batch_send_messages(queue_name, items):
    """

    :param queue_name:
    :param items: 消息集合
    {
        'Id':'1',
        'MessageBody':'Hello',
        'MessageAttributes':{
            'Author' : {
                'StringValue':'SKYFREE',
                'DataType' :'String'
            }
        }
    }
    :return: 返回任何可能的错误
    """
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    response = queue.send_messages(Entries=items)

    # 打印出成功的记录
    # print response.get('Successful')

    # 打印出所有失败的情况
    return response.get('Failed')


def sqs_process_messages(queue_name):
    sqs = boto3.resource('s3')
    queue = sqs.get_queue_by_name(queue_name)

    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        author_text = ''
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')

            if author_name:
                author_text = ' ({0})'.format(author_name)

        print 'Hello, {0}!{1}'.format(message.body, author_text)

        # 成功处理完消息后就删除, 类似ACK
        message.delete()


if __name__ == '__main__':
    print sqs_get_all_queues()
