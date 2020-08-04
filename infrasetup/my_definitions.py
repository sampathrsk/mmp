import collections
import boto3
import psycopg2
import pprint
from botocore.exceptions import ClientError
#import views
import sys

import logging
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
elb = boto3.client('elb')
autoscaling = boto3.client('autoscaling')
keyname = 'sample'

def user_data_fetch(flag):
    try:
	if flag == 'main':
		with open("script.txt",'r') as i:
    			lines = i.readlines()
	else:
		with open("subordinate-script.txt",'r') as i:
			lines = i.readlines()
	x = ''
	for i in lines:
		x=x+i
	return x
    except Exception as e:
           logging.exception(e) 

def ami_fetch(reg,ver):
 from urllib import quote
 import urllib
 import urlparse
 import os
 import pprint
 a='release'
 b=ver
 if (b=='16.04 LTS'):
    d='xenial'
 elif(b=='14.04 LTS'):
    d='trusty'
 elif (b=='12.04 LTS'):
    d='precise'
 elif (b=='16.10'):
    d='yakkety'
 elif (b=='17.04'):
    d='zesty'
 c='server'
 #ternary operator gives either released.txt(alpha1 tag) or released.current.txt(release tag)
 query_file=('released' if a=='release'or'alpha1' else '')+('' if a is not 'release' else '.current')+'.txt'
 link = "http://cloud-images.ubuntu.com/query/{}/{}/{}".format(
    quote(d), quote(c), quote(query_file))
 #link="http://cloud-images.ubuntu.com/query/precise/server/released.current.txt"
 f = urllib.urlopen(link)
 myfile = f.read()
 #myfile gives all the content of the above link variable

 os.system("touch myfile.txt")#txt file to store data
 #os.system("touch myfile.csv")#csv file to store data in csv format
 fl=open("myfile.txt","r+")
 fl.writelines(myfile)
 infile = open("myfile.txt","r")
 mumbai = []
 for aline in infile:
    items = aline.split()
    if(items[0]!='abd'):
   	 if(items[6]==reg and items[8]=='hvm'):
      	 	a=items[7]
      	 	mumbai.append(a)
 return mumbai[0]
 infile.close()

def describe_vpcs(ec2):
    try:
        vpc = list(ec2.vpcs.all())
        Noofvpcs = len(vpc)
        response = []
        for i in range(0,Noofvpcs):
                if vpc[i].is_default == True:
                        if vpc[i].tags == None:
                                tag = vpc[i].create_tags(Tags = [{'Key':'Name','Value':'default_vpc'},])
                        response.append('default_vpc')
                else:
                        response.append(vpc[i].tags[0]['Value'])
        return (response)
    except Exception as e:
           logging.exception(e)
#abc=describe_vpcs(ec2)
#pprint.pprint(abc)
def describe_autoscaling_groups(autoscaling):
    try:
        autoscalinggroups = autoscaling.describe_auto_scaling_groups()
        length = len(autoscalinggroups['AutoScalingGroups'])
        response = []
        for i in range(0,length):
                response.append(autoscalinggroups['AutoScalingGroups'][i]['Tags'][0]['ResourceId'])

        return (response)
    except Exception as e:
           logging.exception(e)
def describe_autoscaling_launchconfigurations(autoscaling):
    try:
        launchconfigurations = autoscaling.describe_launch_configurations()
        length = len(launchconfigurations['LaunchConfigurations'])
        response = []
        for i in range(0,length):
                response.append(launchconfigurations['LaunchConfigurations'][i]['LaunchConfigurationName'])

        return (response)
    except Exception as e:
           logging.exception(e)  
def CreateSubnet(client,vpc):
    try:
        response = client.describe_availability_zones()
        noofavailzones = len(response['AvailabilityZones'])
        Cidrlist = []
        Cidrlist.extend(('10.0.1.0/24','10.0.2.0/24','10.0.3.0/24','10.0.4.0/24'))
        subnets = []
        for i in range(0,noofavailzones):
                subnet = vpc.create_subnet(
                        AvailabilityZone = response['AvailabilityZones'][i]['ZoneName'],
                        CidrBlock = Cidrlist[i],
                        )
                subnets.append(subnet.id)
        return subnets
    except Exception as e:
           logging.exception(e)    

def CreateVpc(ec2):
    try:
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc.modify_attribute(
                EnableDnsHostnames={'Value':True})
        vpc.wait_until_available()
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value':'test_vpc'},])
        return vpc
    except Exception as e:
           logging.exception(e)

def InternetGateway(ec2,vpc):
    try:
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        return ig
    except Exception as e:
           logging.exception(e)

def Routetable(vpc,ig):
    try:
        route_table = vpc.create_route_table()
        route_table.create_tags(Tags=[{'Key':'Name','Value':'routetable'}])
        route = route_table.create_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    GatewayId=ig.id
                )
        return route_table
    except Exception as e:
           logging.exception(e)  

def SubnetRoutetableassociation(subnets,route_table):
    try:
        Noofsubnets = len(subnets)
        for i in range(0,Noofsubnets):
                route_table.associate_with_subnet(SubnetId=subnets[i])
    except Exception as e:
           logging.exception(e)  

def CreateInstances(ec2,subnets,sec_group,Keyname,instancetype,max_count,client,image_id):

        try:
                key = client.describe_key_pairs(KeyNames=[Keyname])
                print 'keypair already exists'
        except ClientError as e:
                if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
                        key = client.create_key_pair(KeyName=keyname)

        instance_id = []
        for i in range(1,max_count+1):
                if i%2 == 0:
                        instances = ec2.create_instances(
                                ImageId= image_id,
                                MinCount= 1,
                                MaxCount= 1,
                                KeyName= Keyname,
                                InstanceType= instancetype,
                                NetworkInterfaces=[{'AssociatePublicIpAddress': True,'DeviceIndex': 0,'SubnetId':subnets[0],'Groups':[sec_group]}],
                                )
                        instance_id.append(instances[0].id)
                        ec2.create_tags(Resources=[instances[0].id],Tags=[{'Key':'Name','Value':('test'+' '+ str(i))}])
                else:
                        instances = ec2.create_instances(
                                ImageId= image_id,
                                MinCount= 1,
                                MaxCount= 1,
                                KeyName= Keyname,
                                InstanceType= instancetype,
                                NetworkInterfaces=[{'AssociatePublicIpAddress': True,'DeviceIndex': 0,'SubnetId':subnets[1],'Groups':[sec_group]}],
                                )
                        instance_id.append(instances[0].id)
                        ec2.create_tags(Resources=[instances[0].id],Tags=[{'Key':'Name','Value':('test'+' '+ str(i))}])
        return instance_id

def CreateSecurityGroup(ec2,vpc):
    try:
        sec_group = ec2.create_security_group(
                GroupName = 'securitydemo1', Description = 'SecurityGroup for demo', VpcId = vpc.id)
        ip_ranges = [{'CidrIp': '0.0.0.0/0'}]
        sec_group.authorize_ingress(
                IpPermissions = [{
                'IpProtocol' : 'TCP',
                'FromPort' : 22,
                'ToPort' : 22,
                'IpRanges': ip_ranges},{
                'IpProtocol' : 'TCP',
                'FromPort' : 80,
                'ToPort' : 80,
                'IpRanges': ip_ranges},{
                'IpProtocol' : 'TCP',
                'FromPort' : 443,
                'ToPort' : 443,
                'IpRanges' : ip_ranges}])
        sec_group_id = sec_group.group_id
        return sec_group_id
    except Exception as e:
           logging.exception(e)  

def CreateELB(elb,sec_group,subnets,name):
    try:
        response = elb.create_load_balancer(
                Listeners=[
                        {
                                'InstancePort': 80,
                                'InstanceProtocol': 'Http',
                                'LoadBalancerPort': 80,
                                'Protocol': 'Http',
                        },
                ],
                LoadBalancerName = name,
                SecurityGroups=[
                        sec_group,
                ],
                Scheme = 'internal',
                Subnets=[
                        subnets[0],subnets[1],
                ],
                )
    except Exception as e:
           logging.exception(e)    

def CreateHealthCheck(elb):
    try:
       response = elb.configure_health_check(
                       LoadBalancerName = 'my-load-balancer',
                       HealthCheck={
                               'Target':'HTTP:80/png',
                               'HealthyThreshold': 2,
                               'Interval': 45,
                               'Timeout': 3,
                               'UnhealthyThreshold': 2,})

    except Exception as e:
           logging.exception(e)

def CreateLaunchConfiguration(autoscaling,image_id,instancetype,sec_group,name,keyname,lines):
    try:
        response = autoscaling.create_launch_configuration(
                ImageId = image_id,
		KeyName = keyname,
                InstanceType = instancetype,
                LaunchConfigurationName = name,
		AssociatePublicIpAddress=True,
		UserData = lines,
                SecurityGroups=[sec_group,],)
    except Exception as e:
           logging.exception(e)

def CreateAutoScalingGroup(autoscaling,subnets,max_count,launch_config,name):
    try:
	response = autoscaling.create_auto_scaling_group(
                AutoScalingGroupName = name,
                LaunchConfigurationName = name,
                MaxSize = max_count+1,
                MinSize = max_count,
                #HealthCheckGracePeriod = 120,
                #HealthCheckType = 'ELB',
                LoadBalancerNames = [name],
                VPCZoneIdentifier = ''+subnets[0]+','+subnets[1]+'',
                )
    except Exception as e:
           logging.exception(e)

def CreateTags(autoscaling,name,ASG):
    try:
        response = autoscaling.create_or_update_tags(
                Tags=[{
                        'ResourceId':ASG,
                        'ResourceType':'auto-scaling-group',
                        'Key':'Name',
                        'Value': name,
                        'PropagateAtLaunch': True},])
    except Exception as e:
           logging.exception(e)

def ifvpcexists(vpc,ec2):
    try:
	vpc1 = list(ec2.vpcs.filter(Filters=[{'Name':'tag:Name','Values':[vpc]}]))
	vpc = vpc1[0]
        subnets = list(vpc.subnets.all())
        subnetid = []
        for i in subnets:
                subnetid.append(i.id)
        sec_groups = list(vpc.security_groups.all())
        sec_group_id = sec_groups[1].group_id
        response = {'Subnets':subnetid,'Sec_groups':sec_group_id}
        return response

    except Exception as e:
           logging.exception(e)







