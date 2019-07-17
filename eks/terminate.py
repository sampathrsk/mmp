import boto3
import time
#cloudformation = boto3.client('cloudformation',region_name='us-west-2')
#eks = boto3.client('eks',region_name='us-west-2')

def delete_cluster(eks,cluster_name):
    response=eks.delete_cluster(
        name=cluster_name
    )
    return response

def delete_stack(cloudformation,stack_name_workernodes):
    response = cloudformation.delete_stack(
        StackName=stack_name_workernodes,
    )
    return response

#stack_name = input('Enter the stack name:')
#cluster_name = input('Enter the name of the eks cluster:')
#stack_name_workernodes = input('stack name of the workers:')

#workerstacktermination=delete_stack(cloudformation,stack_name_workernodes)
#print workerstacktermination
#clusterdelete=delete_cluster(eks,cluster_name)
#time.sleep(120)
#masterstacktermination=delete_stack(cloudformation,stack_name)
