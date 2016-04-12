#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 15:40
import boto3


# S3中使用分页器获取object, 默认每次返回1000个对象
def s3_paginator(bucket_name):
    s3 = boto3.client("s3", region_name='ap-northeast-1')

    paginator = s3.get_paginator('list_objects')

    page_iterator = paginator.paginate(Bucket=bucket_name)

    for page in page_iterator:
        print len(page['Contents'])


# 自定义分页大小
def s3_pagesize_paginator(bucket_name, page_size=500):
    s3 = boto3.client("s3", region_name='ap-northeast-1')

    paginator = s3.get_paginator('list_objects')

    page_iterator = paginator.paginate(Bucket=bucket_name, PaginationConfig={'PageSize': page_size})

    for page in page_iterator:
        print len(page['Contents'])


# 定义返回记录条数
def s3_top_n_paginator(bucket_name, max_items=10):
    s3 = boto3.client("s3", region_name='ap-northeast-1')

    paginator = s3.get_paginator('list_objects')

    page_iterator = paginator.paginate(Bucket=bucket_name, PaginationConfig={'MaxItems': max_items})

    for page in page_iterator:
        print len(page['Contents'])


# 过滤结果
def s3_filter_paginator(bucket_name, prefix="assets"):
    s3 = boto3.client("s3", region_name='ap-northeast-1')

    paginator = s3.get_paginator('list_objects')

    operation_parameters = {
        'Bucket': bucket_name,
        'Prefix': prefix,
        # 这是每次分页的数目
        'MaxKeys': 10
    }

    page_iterator = paginator.paginate(**operation_parameters)

    for page in page_iterator:
        print len(page['Contents'])
        # for item in page['Contents']:
        #    print item['Key']


# JMESPath: json的查询语言, 可以理解为是客户端排序
def s3_jmespath_sort(bucket_name):
    s3 = boto3.client("s3", region_name='ap-northeast-1')

    paginator = s3.get_paginator('list_objects')

    page_iterator = paginator.paginate(Bucket=bucket_name)

    filtered_iterator = page_iterator.search('Contents[?Size > `100`][]')
    for key_data in filtered_iterator:
        print key_data


if __name__ == '__main__':
    s3_jmespath_sort("anti-theft-static.skyfree.com.cn")
