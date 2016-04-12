#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 11:10
import boto3
import os
from botocore.exceptions import ClientError


def s3_create_bucket(bucket_name, region="ap-northeast-1"):
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
        'LocationConstraint': region
    })
    bucket = s3_get_bucket(bucket_name)

    # 可以保证一定是创建好了该bucket才继续
    bucket.wait_until_exists()


def s3_get_all_buckets():
    s3 = boto3.resource('s3')

    ret = []
    for bucket in s3.buckets.all():
        ret.append(bucket.name)

    return ret


def s3_upload_file(bucket_name, file_path):
    s3 = boto3.resource('s3')
    data = open(file_path, 'rb')
    file_name = os.path.basename(file_path)

    # 两种写法
    # s3.Bucket(bucket_name).put_object(Key=file_name, Body=data)
    s3.Object(bucket_name, file_name).put(Body=data)


def s3_is_exist_bucket(bucket_name):
    s3 = boto3.resource('s3')
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

    return exists


def s3_get_bucket(bucket_name):
    # 从Bucket资源直接获取object: bucket.Object(key='xxx')
    return boto3.resource('s3').Bucket(bucket_name)


def s3_get_object(bucket_name, key):
    s3 = boto3.resource('s3')

    # obj.bucket_name, obj.key
    # 等同于: s3.Object(bucket_name, key)
    return s3.Object(bucket_name=bucket_name, key=key)


def s3_get_object_string(bucket_name, key):
    obj = s3_get_object(bucket_name, key)
    response = obj.get()
    return response['Body'].read()


def s3_delete_bucket(bucket_name):
    bucket = s3_get_bucket(bucket_name)

    for key in bucket.objects.all():
        key.delete()

    bucket.delete()


def s3_get_all_keys(bucket_name):
    bucket = s3_get_bucket(bucket_name)

    ret = []
    for key in bucket.objects.all():
        ret.append(key.key)

    return ret


def s3_get_all_acls(bucket_name):
    bucket = s3_get_bucket(bucket_name)

    acl = bucket.Acl()
    for grant in acl.grants:
        print grant['Grantee'].get('DisplayName'), grant['Permission']


def s3_set_public_read(bucket_name):
    bucket = s3_get_bucket(bucket_name)
    bucket.Acl().put(ACL='public-read')


# 如果获取到key, 需要查下手册
def s3_set_key_metadata(key, metadata):
    """

    :param key:
    :param metadata:
    例如: {
        "meta1":"This is my metadata value"
    }
    :return:
    """
    key.put(Metadata=metadata)


def s3_get_cors(bucket_name):
    bucket = s3_get_bucket(bucket_name)
    cors = bucket.Cors()
    return cors.cors_rules


def s3_set_cors(bucket_name, cors_config):
    """

    :param bucket_name:
    :param cors_config:
    例如:
    {
        'CORSRules':[
            {
                'AllowedMethods':['GET'],
                'AllowedOrigins':['*']
            }
        ]
    }
    :return:
    """
    bucket = s3_get_bucket(bucket_name)
    cors = bucket.Cors()
    cors.put(CORSConfiguration=cors_config)


def s3_clear_cors(bucket_name):
    bucket = s3_get_bucket(bucket_name)
    bucket.Cors().delete()
