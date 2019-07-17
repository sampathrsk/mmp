from my_definitions import CreateVpc
from my_definitions import CreateSubnet
from my_definitions import InternetGateway
from my_definitions import Routetable
from my_definitions import SubnetRoutetableassociation
from my_definitions import CreateSecurityGroup
from my_definitions import ami_fetch
from my_definitions import CreateInstances
from my_definitions import CreateELB
from my_definitions import CreateLaunchConfiguration
from my_definitions import CreateAutoScalingGroup
#from my_definitions_new import CreateHealthCheck
from my_definitions import ifvpcexists
from my_definitions import CreateTags
from my_definitions import user_data_fetch

import boto3
import sys
from botocore.exceptions import ClientError

import logging
keyname = 'sample'

def instance_provisioning(reg,vpc,ver,instancetype,ec2,client,elb,autoscaling,launch_config,max_count,flag,ASG):
    try:
	if flag == 'slave' and vpc == 'Create new':
		vpc = 'test_vpc'
	if vpc != "Create new":
	        response = ifvpcexists(vpc,ec2)
	        subnets = response['Subnets']
	        sec_group = response['Sec_groups']
	        #image_id = ami_fetch(reg,ver)
                image_id = 'ami-44273924'
	        Elb = CreateELB(elb,sec_group,subnets,ASG)
		lines = user_data_fetch(flag)
	        if launch_config == "Create new":
			LaunchConfiguration = CreateLaunchConfiguration(autoscaling,image_id,instancetype,sec_group,ASG,keyname,lines)
		Autoscalinggroup = CreateAutoScalingGroup(autoscaling,subnets,max_count,launch_config,ASG)
		createtags = CreateTags(autoscaling,flag,ASG)
	else:
	        vpc = CreateVpc(ec2)
	        subnets = CreateSubnet(client,vpc)
	        ig = InternetGateway(ec2,vpc)
	        routetable = Routetable(vpc,ig)
	        SubnetRoutetableassociation(subnets,routetable)
	        sec_group = CreateSecurityGroup(ec2,vpc)
	        #image_id = ami_fetch(reg,ver)
		image_id = 'ami-44273924'
	        Elb = CreateELB(elb,sec_group,subnets,ASG)
		lines = user_data_fetch(flag)
	        if launch_config == "Create new":
			LaunchConfiguration = CreateLaunchConfiguration(autoscaling,image_id,instancetype,sec_group,ASG,keyname,lines)
		Autoscalinggroup = CreateAutoScalingGroup(autoscaling,subnets,max_count,launch_config,ASG)
		createtags = CreateTags(autoscaling,flag,ASG)
    except Exception as e:
           logging.exception(e)
