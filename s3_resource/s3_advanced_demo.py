#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/13 11:19
"""
Addressing Style
S3支持两种形式
    1. Virtual Host Style
    2. Path Style
"""
import boto3
from botocore.client import Config


def s3_set_addressing_style():
    # 合法选项: auto, virtual, path
    s3 = boto3.client('s3', 'ap-northeast-1', config=Config(s3={'addressing_style': 'path'}))
    pass


"""
使用Transfer Manager
主要是使上传和下载文件更加方便
"""


def s3_client_upload_and_download():
    s3 = boto3.client('s3')
    s3.upload_file('/path/to/tmp.txt', "bucket-name", 'key-name')
    s3.download_file('bucket-name', 'key-name', 'path/to/download.txt')


def s3_resource_upload_and_download():
    s3 = boto3.resource('s3')

    bucket = s3.Bucket('bucket-name')
    obj = bucket.Objcet('key-name')

    obj.upload_file('/local/path/to/file')
    obj.download_file('/local/path/to/download/file')


"""
生成 Presigned URL: 可以理解为百度网盘的公开访问链接
"""


# 可以理解为读操作
def s3_get_presigned_url():
    s3 = boto3.client('s3')

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'skyfree-test',
            'Key': 'aws cluster management.jpg'
        }
    )

    return url


# 可以理解为读操作
# 使用signature version 4
def s3_get_presigned_url_with_ver4():
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))

    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': 'skyfree-test',
            'Key': 'aws cluster management.jpg'
        }
    )

    return url


"""
Presigned POSTS: 可以理解为公开访问链接, 具有写入的权限
"""


def s3_post_presigned_url():
    s3 = boto3.client('s3')

    post = s3.generate_presigned_post(Bucket='skyfree-test', Key='test-post-data.txt')

    return post['url'], post['fields']


def test_s3_post_presigned_url():
    import requests
    files = {"file": "hello s3, I am from post request!"}

    url, fields = s3_post_presigned_url()
    response = requests.post(url, data=fields, files=files)

    print response.status_code
