#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 14:54

#  多线程创建多个资源
import threading

import boto3

"""
boto3 Session: 可以控制以下信息
    Credentials
    Region
    其他配置项
"""


# 多线程的写法
class MyTask(threading.Thread):
    def run(self):
        session = boto3.session.Session()
        s3 = session.resource('s3')
        # 创建各类aws资源


# 默认session
def sqs_get_default_session():
    return boto3.resource("sqs")


# 获取自定义session
def sqs_get_custom_session():
    session = boto3.session.Session()
    sqs = session.resource("sqs")
    return sqs.queues.all()


if __name__ == '__main__':
    print list(sqs_get_custom_session())[0].url
