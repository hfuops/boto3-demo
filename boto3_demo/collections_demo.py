#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 14:57
import boto3


# Get ALL
def sqs_get_all_queues():
    sqs = boto3.resource('sqs')
    for queue in sqs.queues.all():
        print queue.url


# 转化为List
def s3_get_bucket_count():
    s3 = boto3.resource('s3')
    buckets = list(s3.buckets.all())
    return len(buckets)


# 批量处理, 清空bucket
def s3_clear_bucket(bucket_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).objects.delete()


# 过滤, s3上以prefix过滤 (当s3文件数很多时, 下面的操作会非常费钱的)
def s3_filter_by_prefix(bucket_name, prefix='/logs'):
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        for obj in bucket.objcets.filter(Prefix=prefix):
            print "{0}:{1}".format(bucket_name, obj.key)


# 链式调用演示
def ec2_filter_demo():
    ec2 = boto3.resource('ec2')

    # 通过instance id list过滤
    base = ec2.instances.filter(InstanceIds=["i-1a67dd", "i-6j89k", "i-xx8x"])

    filters = [
        {
            "name": "tenancy",
            "value": "dedicated"
        }
    ]

    # 继续过滤
    filtered1 = base.filter(Filters=filters)

    filters.append({
        "name": "instance-type",
        "value": "t1.micro"
    })

    filtered2 = base.filter(Filters=filters)

    for instance in base:
        print instance.id

    for instance in filtered1:
        print instance.id

    for instance in filtered2:
        print instance.id


# top N
def s3_get_top_5_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.limit(5):
        print bucket.name


# 控制分页大小
def s3_get_objects_with_pagesize(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for obj in bucket.objcets.page_size(100):
        print obj.key


# 批量处理, 清空bucket
def s3_clear_all_bucket(bucket_name):
    s3 = boto3.resource('s3')
    s3.buckets(bucket_name).objects.delete()
