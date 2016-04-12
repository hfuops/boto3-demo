#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 15:27
import boto3

"""
low api: 与aws的api是一对一的关系
服务操作与client的底层操作的方法和方法签名是一致的,
但是参数全部为命名参数, 没有位置参数
"""


# 获取sqs的low api
def get_sqs_client():
    return boto3.client('sqs')


# 通过resource获取sqs的low api
def get_sqs_client_by_resource():
    sqs = boto3.resource('sqs')
    return sqs.meta.client


# 处理响应
def sqs_get_all_queues():
    sqs = get_sqs_client()

    response = sqs.list_queues()
    print response

    for url in response.get("QueueUrls", []):
        print url


# waiter

# 获取s3可以使用的所有waiter
# [u'bucket_exists', u'bucket_not_exists', u'object_exists', u'object_not_exists']
def get_all_s3_waiters():
    s3 = boto3.client('s3')
    return s3.waiter_names


# 在S3中使用waiter
def s3_waiter_bucket_ready(bucket_name):
    s3 = boto3.client('s3')
    s3_bucket_exists_waiter = s3.get_waiter("bucket_exists")
    s3_bucket_exists_waiter.wait(Bucket=bucket_name)


# 获取sqs可以使用的所有waiter
def get_all_sqs_waiters():
    sqs = boto3.client('sqs')
    return sqs.waiter_names
