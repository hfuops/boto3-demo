#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 16:10
"""
访问AWS的最少参数:
aws_access_key_id
aws_secret_access_key
region

# 配置方法 1
aws configure
保存位置: ~/.aws

boto3 认证信息的搜索路径, 找到即停止搜索
1. 直接向boto3.client()提供认证参数
2. 创建Session对象时, 提供认证参数
3. 环境变量
4. ~/.aws/credentials
5. Assume Role provider
6. /etc/boto.cfg 和 ~/.boto
7. Instance metadata (IAM中设置的)

"""

import boto3


# 1. 直接传递认证信息
# session_token为可选项
def s3_client(access_key, secret_key, session_token):
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )
    return client


def s3_session(access_key, secret_key, session_token):
    client = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )
    return client


# 2. 环境变量
"""
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# 与临时认证有关
AWS_SESSION_TOKEN
"""

# 3 ~/.aws/credentials
"""
默认是保存在: ~/.aws/credentials
[default]
aws_access_key_id=foo
aws_secret_access_key=bar
aws_session_token=baz

可以指定环境变量指定配置文件的新位置:
AWS_SHARED_CREDENTIALS_FILE


# profile的支持
===============================
[default]
aws_access_key_id=foo
aws_secret_access_key=bar

[dev]
aws_access_key_id=foo2
aws_secret_access_key=bar2

[prod]
aws_access_key_id=foo3
aws_secret_access_key=bar3

使用不同的profile
    session = boto3.Session(profile_name = 'dev')
    dev_s3 = session.client('s3')
"""

# 4. ~/.aws/config
"""
通过环境变量修改config的路径:
AWS_CONFIG_FILE

[default]
aws_access_key_id=foo
aws_secret_access_key=bar

[profile dev]
aws_access_key_id=foo2
aws_secret_access_key=bar2

[profile prod]
aws_access_key_id=foo3
aws_secret_access_key=bar3

内容与~/.aws/credentials基本类似, 就是编写profile时,必须要以包含profile前缀
"""

# 5. Assume Role Provider (角色假定)
"""
5.1 配置位置:  ~/.aws/config 可以在这里配置假定角色

cat ~/.aws/credentials
[development]
aws_access_key_id=foo
aws_secret_access_key=bar

cat ~/.aws/config
[profile crossaccount]
role_arn=arn:aws:iam:...
source_profile=development

~/.aws/config的配置选项说明:
    role_arn: 角色的ARN
    source_profile: 包括了认证信息aws_access_key_id, aws_secret_access_key

    external_id:
    mfa_serial: MFS的串号
    role_session_name: session的名称

    如果没有启用MFA认证, 只需要提供role_arn和source_profile
"""

# 6. 尝试加载boto2配置
"""
位置: /etc/boto.cfg, ~/.boto
cat ~/.boto
[Credentials]
aws_access_key_id = foo
aws_secret_access_key = bar
"""

# 7. IAM
"""
如果本地没有任何AWS的认证信息, boto3会尝试从instance metadata加载认证信息
前提: 当用户启动EC2实例时, 必须指定IAM Role
"""

# 8. 最佳实践
"""
如果使用EC2实例, 使用IAM的Role
否则使用~/.aws/credentials
"""

# ================== 配置 =====================
"""
指定配置的方法:
    1. 创建client时, 指定config参数
    2. 环境变量
    3. ~/.aws/config

支持的环境变量
    AWS_ACCESS_KEY_ID:
    AWS_SECRET_ACCESS_ID:
    AWS_SESSION_TOKEN: 仅在临时认证时, 才会用到
    AWS_DEFAULT_REGION
    AWS_PROFILE

    AWS_CONFIG_FILE
    AWS_SHARED_CREDENTIALS_FILE

    AWS_CA_BUNDLE: 使用SSL/TLS时, 指定证书位置
    AWS_METADATA_SERVICE_TIMEOUT: Assume Role Provider时的超时设置, 默认是1秒, 单位秒
    AWS_METADATA_SERVICE_NUM_ATTEMPTS: 尝试的连接次数
    AWS_DATA_PATH: 搜索路径, Linux使用:分割,一般不设置. 默认搜索: <botocoreroot>/data/ 和 ~/.aws/models

~/.aws/config中支持的选项
    注意: 至少要保证有[default]的section

    region: 指定区域:ap-northeast-1
    aws_access_key_id
    aws_secret_access_id
    aws_session_token
    ca_bundle
    metadata_service_timeout
    metadata_service_num_attempts
    role_arn
    source_profile
    external_id
    mfa_serial
    role_session_name
    s3: 一般不用理会, boto3会处理的

"""

