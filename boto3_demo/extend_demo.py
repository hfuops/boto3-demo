#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 16:54
"""
因为boto3使用了类似工厂模式, 所有对象都是runtime时生成的, 这也就无法使用常规的继承手段进行扩展了
只能通过Boto3提供的事件系统进行扩展 (类似SharePoint中的EventHandler)

1. 介绍
    Boto3允许用户在某些事件上注册handler
    调用顺序, 按照注册的顺序, 依次进行

"""

# 对S3的listObjects事件进行注册
import boto3
from boto3.session import Session


def s3_register_handler(s3_client):
    event_system = s3_client.meta.events

    # 注意kwargs是必须的, 即使没有使用该变量
    def add_my_bucket(params, **kwargs):
        if 'Bucket' not in params:
            params['Bucket'] = 'anti-theft-static.skyfree.com.cn'

    event_system.register('provide-client-params.s3.ListObjects', add_my_bucket)


def s3_trigger_list_object_event():
    s3 = boto3.client("s3")
    s3_register_handler(s3)

    # 这里我们并没有指定操作哪个bucket, handler会自动帮我们增加Bucket参数
    print s3.list_objects()


"""
2. 事件系统的继承结构
    使用"."表示层次关系
    例如:
        general.specific.more_specific
        general.specific
        general

        按最精确的匹配走
"""


def s3_register_handlers(s3):
    event_system = s3.meta.events

    def add_my_general_bucket(params, **kwargs):
        if 'Bucket' not in params:
            params['Bucket'] = 'skyfree-test'

    def add_my_specific_bucket(params, **kwargs):
        if 'Bucket' not in params:
            params['Bucket'] = 'anti-theft-static.skyfree.com.cn'

    event_system.register('provide-client-params.s3', add_my_general_bucket)
    event_system.register('provide-client-params.s3.ListObjects', add_my_specific_bucket)


def s3_trigger_handers():
    s3 = boto3.client('s3')
    s3_register_handlers(s3)

    # 最精确匹配, 所以会使用anti-theft-static.skyfree.com.cn的bucket
    print s3.list_objects()

    # 模糊匹配,
    print s3.put_object(Key="mydata", Body=b'abc123')


"""
通配匹配
"""


def s3_register_wildcard_handler(s3):
    event_system = s3.meta.events

    def add_my_wildcard_bucket(params, **kwargs):
        if 'Bucket' not in params:
            params['Bucket'] = 'skyfree-test'

    # provide-client-params.s3.*objects
    event_system.register('provide-client-params.s3.*', add_my_wildcard_bucket)


def s3_trigger_wildcard_handler():
    s3 = boto3.client('s3')
    s3_register_wildcard_handler(s3)

    print s3.list_objects()


"""
事件的隔离范围
    每个boto3.client()会使用单独的事件系统
"""

"""
boto3的事件类型
    create-client-class.service_name: 在创建资源是触发事件, 比如调用: boto3.client('s3')
    create-resource-class.service_name.resource_name: 创建资源时,触发事件
    provide-client-params.service_name.operation_name: 具体操作时, 触发事件
"""


# create-client-class
# 增加一个新的方法
def s3_create_client_class_register_method():
    # 这个方法参数是必须的
    # noinspection PyUnusedLocal
    def custom_method(self):
        print "I am from s3_create_client_class_register.custom_method"

    # noinspection PyUnusedLocal
    def add_custom_method(class_attributes, **kwargs):
        class_attributes['my_method'] = custom_method

    session = Session()
    session.events.register('creating-client-class.s3', add_custom_method)

    # 一定要返回这个会话
    return session


def s3_invoke_customer_method():
    session = s3_create_client_class_register_method()
    s3 = session.client('s3')
    s3.my_method()


# 创建一个新的类
def s3_create_client_class_register_new_class():
    # 先定义一个新类
    class MyClass(object):
        def __init__(self, *args, **kwargs):
            super(MyClass, self).__init__(*args, **kwargs)
            print "Client instantiated!"

    def add_custom_class(base_classes, **kwargs):
        base_classes.insert(0, MyClass)

    session = Session()
    session.events.register('creating-client-class.s3', add_custom_class)

    return session


def s3_invoke_custom_class():
    session = s3_create_client_class_register_new_class()
    s3 = session.client('s3')

if __name__ == '__main__':
    s3_invoke_custom_class()