import boto3
import pprint
reg='ap-southeast-1'
ec2 = boto3.resource('ec2', region_name=reg)
client = boto3.client('ec2', region_name=reg)
from botocore.exceptions import ClientError

def CreateSubnet(vpc):
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

def CreateVpc(vpcname,ec2):
        vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc.modify_attribute(
                EnableDnsHostnames={'Value':True})
        vpc.wait_until_available()
        vpc.create_tags(Tags=[{'Key': 'Name', 'Value':vpcname},])
        return vpc

def InternetGateway(ec2,vpc):
        ig = ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        return ig

def Routetable(vpc,ig):
        route_table = vpc.create_route_table()
        route_table.create_tags(Tags=[{'Key':'Name','Value':'routetable'}])
        route = route_table.create_route(
                    DestinationCidrBlock='0.0.0.0/0',
                    GatewayId=ig.id
                )
        return route_table

def SubnetRoutetableassociation(subnets,route_table):
        Noofsubnets = len(subnets)
        for i in range(0,Noofsubnets):
                route_table.associate_with_subnet(SubnetId=subnets[i])

def ifvpcexists(vpcname,ec2):
        vpc1 = list(ec2.vpcs.filter(Filters=[{'Name':'tag:Name','Values':[vpcname]}]))
        vpc = vpc1[0]
        subnets = list(vpc.subnets.all())
        subnetid = []
        for i in subnets:
                subnetid.append(i.id)
        sec_groups = list(vpc.security_groups.all())
        sec_group_id = sec_groups[1].group_id
        response = {'Subnets':subnetid,'Sec_groups':sec_group_id}
        return response

def CreateSecurityGroup(ec2,vpc):
        sec_group = ec2.create_security_group(
                GroupName = 'Fargate_sg', Description = 'sg for fargate', VpcId = vpc.id)
        ip_ranges = [{'CidrIp': '0.0.0.0/0'}]
        sec_group.authorize_ingress(
                IpPermissions = [{
                'IpProtocol' : 'TCP',
                'FromPort' : 80,
                'ToPort' : 80,
                'IpRanges': ip_ranges}])
        sec_group_id = sec_group.group_id
        return sec_group_id

def create_fargate_vpc(vpcname,ec2):
                vpc1= client.describe_vpcs(Filters = [{'Name':'tag:Name', 'Values':[vpcname]}])
                if (vpc1['Vpcs']==[]):
                  vpc=CreateVpc(vpcname,ec2)
                  subnets=CreateSubnet(vpc)
                  ig=InternetGateway(ec2,vpc)
                  route_table=Routetable(vpc,ig)
                  SubnetRoutetableassociation(subnets,route_table)
                  sg=CreateSecurityGroup(ec2,vpc)
                  print('creating new vpc')
                  response = {'Subnets':subnets,'Sec_groups':sg}
                  return response
                else:
                   print('vpc already exists')
                   response=ifvpcexists(vpcname,ec2)
                   return response
#fargate=create_fargate_vpc('vpc',ec2)
#pprint.pprint(fargate)

