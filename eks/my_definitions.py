import boto3
import subprocess
import json
import time
import yaml
import ruamel.yaml

iam = boto3.client('iam')
cloudformation = boto3.client('cloudformation',region_name='us-west-2')
eks = boto3.client('eks',region_name='us-west-2')
#creating IAM policies for the role to be used by the EKS
#yaml = ruamel.yaml.YAML()
'''
AWSEKSServicePolicy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AttachNetworkInterface",
        "ec2:CreateNetworkInterface",
        "ec2:CreateNetworkInterfacePermission",
        "ec2:DeleteNetworkInterface",
        "ec2:DeleteNetworkInterfacePermission",
        "ec2:Describe*",
        "ec2:DetachNetworkInterface",
        "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
        "elasticloadbalancing:DeregisterTargets",
        "elasticloadbalancing:Describe*",
        "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
        "elasticloadbalancing:RegisterTargets",
        "route53:ChangeResourceRecordSets",
        "route53:CreateHealthCheck",
        "route53:DeleteHealthCheck",
        "route53:Get*",
        "route53:List*",
        "route53:UpdateHealthCheck",
        "servicediscovery:DeregisterInstance",  
        "servicediscovery:Get*",
        "servicediscovery:List*",
        "servicediscovery:RegisterInstance",
        "servicediscovery:UpdateInstanceCustomHealthStatus"
      ],
      "Resource": "*"
    }
  ]
}

AmazonEKSClusterPolicy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:UpdateAutoScalingGroup",
                "ec2:AttachVolume",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateRoute",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:DeleteRoute",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteVolume",
                "ec2:DescribeInstances",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVolumes",
                "ec2:DescribeVolumesModifications",
                "ec2:DescribeVpcs",
                "ec2:DetachVolume",
                "ec2:ModifyInstanceAttribute",
                "ec2:ModifyVolume",
                "ec2:RevokeSecurityGroupIngress",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:ApplySecurityGroupsToLoadBalancer",
                "elasticloadbalancing:AttachLoadBalancerToSubnets",
                "elasticloadbalancing:ConfigureHealthCheck",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateLoadBalancerListeners",
                "elasticloadbalancing:CreateLoadBalancerPolicy",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteLoadBalancerListeners",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:DetachLoadBalancerFromSubnets",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:SetLoadBalancerPoliciesForBackendServer",
                "elasticloadbalancing:SetLoadBalancerPoliciesOfListener",
                "kms:DescribeKey"
            ],
            "Resource": "*"
        }
    ]
}

AssumeRolePolicyDocument = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

def CreatePolicy(iam,AWSEKSServicePolicy):
    policy_name = input('Enter the policy_name:')
    createpolicy = iam.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(AWSEKSServicePolicy),
        Description='policy created specifically for EKS'
    )
    return createpolicy
#crepol=CreatePolicy(iam,AWSEKSServicePolicy)
#print(crepol)

def CreateRole(iam,AssumeRolePolicyDocument):
    createrole = iam.create_role(
        RoleName = 'sample-eks',
        AssumeRolePolicyDocument = json.dumps(AssumeRolePolicyDocument),
        Description = 'Create new role to be used by eks'
    )
    return createrole
#crerol=CreateRole(iam,AssumeRolePolicyDocument)
#print(crerol)
'''
def CreateStack(cloudformation,stack_name):
    response = cloudformation.create_stack(
        StackName=stack_name,
        TemplateURL='https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-vpc-sample.yaml',
        DisableRollback=False,
    )
    return response

def DescribeStackoutputs(cloudformation,stack_name):
    outputs = {}
    response = cloudformation.describe_stacks(
        StackName=stack_name,
    )
    outputs['securitygroup']=response['Stacks'][0]['Outputs'][0]['OutputValue']
    outputs['vpc']=response['Stacks'][0]['Outputs'][1]['OutputValue']
    outputs['subnets']=response['Stacks'][0]['Outputs'][2]['OutputValue']
    return outputs

def createcluster(eks,outputs,cluster_name):
    response = eks.create_cluster(
        name=cluster_name,
        roleArn='arn:aws:iam::367174123714:role/cfs.mmpEKS',
        resourcesVpcConfig={
            'subnetIds':[
                outputs['subnets'][0:24],outputs['subnets'][25:49],outputs['subnets'][50:74],
            ],
            'securityGroupIds':[
                outputs['securitygroup'],
            ]
        }
    )
    return response

def DescribeCluster(eks,cluster_name):
    response = eks.describe_cluster(
        name=cluster_name
    )
    return response

def createstackworkernodes(cloudformation,workers_stack_name,outputs,workernodes,cluster_name):
    workernodes_name = cluster_name+'-worker-nodes'
    response = cloudformation.create_stack(
        StackName=workers_stack_name,
        TemplateURL='https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-06-05/amazon-eks-nodegroup.yaml',
        Parameters=[
            {
                'ParameterKey':'ClusterName',
                'ParameterValue':cluster_name,
            },
            {
                'ParameterKey':'ClusterControlPlaneSecurityGroup',
                'ParameterValue':outputs['securitygroup'],
            },
            {
                'ParameterKey':'NodeGroupName',
                'ParameterValue':workernodes_name,
            },
            {
                'ParameterKey':'NodeAutoScalingGroupMinSize',
                'ParameterValue':'1',
            },
            {
                'ParameterKey':'NodeAutoScalingGroupMaxSize',
                'ParameterValue':workernodes,
            },
            {
                'ParameterKey':'NodeInstanceType',
                'ParameterValue':'t2.large',
            },
            {
                'ParameterKey':'NodeImageId',
                'ParameterValue':'ami-73a6e20b',
            },
            {
                'ParameterKey':'KeyName',
                'ParameterValue':'mmp-eks',
            },
            {
                'ParameterKey':'VpcId',
                'ParameterValue':outputs['vpc'],
            },
            {
                'ParameterKey':'Subnets',
                'ParameterValue':outputs['subnets'][0:24],
            },
            {
                'ParameterKey':'Subnets',
                'ParameterValue':outputs['subnets'][25:49],
            },
            {
                'ParameterKey':'Subnets',
                'ParameterValue':outputs['subnets'][50:74],
            },
        ],
        Capabilities=[
            'CAPABILITY_IAM',
        ],
    )
    return response

def describe_workers_stack(cloudformation,workers_stack_name):
    response=cloudformation.describe_stacks(
        StackName=workers_stack_name,
    )
    #print response['Stacks'][0]
    return response['Stacks'][0]['Outputs'][0]['OutputValue']

def get_externalip(eks):
    externalip=subprocess.call(['./externalip'])
    return externalip

#stack_name = input('Enter the stack name:')
#cluster_name = input('Enter the name of the eks cluster:')
#stack_name_workernodes = input('stack name of the workers:')
#workernodes = input('Please enter the no of worker nodes needed:')
#stackmaster=CreateStack(cloudformation,stack_name)
#time.sleep(120)
#outputs=DescribeStackoutputs(cloudformation,stack_name)
#cluster=createcluster(eks,outputs,cluster_name)
#time.sleep(660)
#clusterinfo=DescribeCluster(eks,cluster_name)
#workerstack=createstackworkernodes(cloudformation,stack_name_workernodes,outputs,workernodes,cluster_name)
#time.sleep(240)
#workerstack_info=describe_workers_stack(cloudformation,stack_name_workernodes)
#print workerstack_info

def config(clusterinfo,cluster_name,workerstack_outputs):
    with open("/root/.kube/config-sample-eks") as f:
        list_doc = yaml.load(f)
    for i in list_doc["clusters"]:
        i["cluster"]["server"]=clusterinfo['cluster']['endpoint']
        i["cluster"]["certificate-authority-data"]=clusterinfo['cluster']['certificateAuthority']['data']
    for i in list_doc["users"]:
        i["user"]["exec"]["args"]=['token','-i',cluster_name]
    with open("/root/.kube/config-sample-eks","w") as f:
        yaml.dump(list_doc, f, default_flow_style=False)
    with open("/home/ubuntu/venv/mmp/aws/aws-auth-cm.yaml") as f:
        list_doc = yaml.load(f)
        list_doc["data"]["mapRoles"] = "- rolearn: "+workerstack_outputs+"\n  username: system:node:{{EC2PrivateDNSName}}\n  groups:\n    - system:bootstrappers\n    - system:nodes\n"
    with open("/home/ubuntu/venv/mmp/aws/aws-auth-cm.yaml","w") as f:
        yaml.dump(list_doc,f)
