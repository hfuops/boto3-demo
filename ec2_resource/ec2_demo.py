#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2015 OPS.
#
# Author: tingfang.bao <tingfang.bao@acadine.com>
# DateTime: 16/4/12 13:17
import boto3


def ec2_run_instances(ami_id, min_count=1, max_count=1):
    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId=ami_id, MinCount=min_count, MaxCount=max_count)


def ec2_stop_instances(instance_ids):
    """

    :param instance_ids: List Type
    :return:
    """
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_ids).stop()


def ec2_terminate_instances(instance_ids):
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_ids).terminate()


def ec2_get_all_running_instances():
    ec2 = boto3.resource('ec2')
    return ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']
    }])


def ec2_get_instance(instance_name):
    ec2 = boto3.resource('ec2')

    # 获取子网资源: instance.subnet
    # 获取vpc: instance.vpc
    # 获取互联网网关: list(instance.vpc.internet_gateways.all())[0].id
    # 在恰当的时候使用: instance.wait_until_running()
    return list(ec2.instances.filter(Filters=[{
        'Name': 'tag:Name',
        'Values': [instance_name]
    }]))[0]


def ec2_get_health_status():
    ec2 = boto3.resource('ec2')
    for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
        print status


def ec2_create_snapshot(volume_id, description):
    ec2 = boto3.resource('ec2')
    ec2.create_snapshot(VolumeId=volume_id, Description=description)


def ec2_create_volume(snapshot_id, availability_zone):
    ec2 = boto3.resource('ec2')
    ec2.create_volume(SnapshotId=snapshot_id, AvailabilityZone=availability_zone)


def ec2_attache_volume(instance_id, volume_id, mount_point='/dev/vdz'):
    ec2 = boto3.resource('ec2')
    ec2.Instance(instance_id).attach_volume(VolumeId=volume_id, Device=mount_point)


def ec2_create_vpc(cidr):
    ec2 = boto3.resource('ec2')
    ec2.create_vpc(CidrBlock=cidr)


def ec2_get_all_vpc():
    ec2 = boto3.resource('ec2')

    # vpc.id, vpc.tags[0]['Value']
    return ec2.vpcs.all()


# noinspection PyBroadException
def ec2_get_vpc(vpc_name):
    ec2 = boto3.resource('ec2')
    filters = [
        {
            "Name": "tag:Name",
            "Values": [vpc_name]
        }
    ]

    try:
        return list(ec2.vpcs.filter(Filters=filters))[0]
    except Exception:
        return None


def ec2_create_subnet(vpc_name, subnet_cidr):
    vpc = ec2_get_vpc(vpc_name)
    vpc.create_subnet(CidrBlock=subnet_cidr)


def ec2_create_internet_gateway():
    ec2 = boto3.resource('ec2')
    ec2.create_internet_gateway()


def ec2_get_internet_gateway():
    ec2 = boto3.resource('ec2')

    # 获取互联网网关id,ec2_get_internet_gateway().id, 我默认只有一个互联网网关
    return list(ec2.internet_gateways.all())[0]


def ec2_attache_internet_gw(vpc_id):
    gw = ec2_get_internet_gateway()
    gw.attche_to_vpc(VpcId=vpc_id)


def ec2_detach_internet_gw(vpc_id):
    gw = ec2_get_internet_gateway()
    gw.detach_from_vpc(VpcId=vpc_id)


def ec2_attach_elastic_ip(eip_id, instance_id):
    ec2 = boto3.resource('ec2')
    address = ec2.VpcAddress(eip_id)
    address.associate(instance_id)


def ec2_detach_elastic_ip(eip_id):
    ec2 = boto3.resource('ec2')
    address = ec2.VpcAddress(eip_id)
    address.association.delete()
