import boto3
import sys
from botocore.exceptions import ClientError
import collections
import pprint
import time

reg='ap-southeast-1'
client = boto3.client('ecs', region_name=reg)
client1 = boto3.client('ec2', region_name=reg)
#cluster_name='ecs-cluster'
#task_definition_name='ecs-fargate-definition'
#service_name='ecs-fargate-service'
#container_name = 'ecs_container'

def create_cluster(cluster_name):
   
        response1 = client.create_cluster(clusterName=cluster_name)
        pprint.pprint(response1)
   

#create_cluster(cluster_name)

def register_task_definition(task_definition_name,container_name):
        response2 = client.register_task_definition(
           family=task_definition_name,
           networkMode='awsvpc',
           #executionRoleArn='arn:aws:iam::915080984106:role/ecsTaskExecutionRole',
           containerDefinitions=[
            {
            'name': container_name,
            'image': 'httpd:2.4',
            'portMappings': [
                {
                    'containerPort': 80,
                    'hostPort': 80,
                    'protocol': 'tcp'
                },
            ],
            'essential': True,
            'entryPoint': [
                'sh',
                '-c'
            ],
            'command': [
                "/bin/sh -c \"echo '<html> <head> <title>Amazon ECS Sample App</title> <style>body {margin-top: 40px; background-color: #333;} </style> </head><body> <div style=color:white;text-align:center> <h1>Amazon ECS Sample App</h1> <h2>Congratulations!</h2> <p>Your application is now running on a container in Amazon ECS.</p> </div></body></html>' >  /usr/local/apache2/htdocs/index.html && httpd-foreground\"",
                ],

        },
            ],
            requiresCompatibilities=[
               'FARGATE',
            ],
            cpu='256',
            memory='512'
            )
        pprint.pprint(response2)
        task_definition=response2['taskDefinition']['taskDefinitionArn']
        #pprint.pprint(task_definition)
        return task_definition
#task_defination=register_task_defination(task_defination_name,container_name)

def create_service(cluster_name,service_name,task_definition,response):
            task_definition =  task_definition
            pprint.pprint(task_definition)
            response3 = client.create_service(
                cluster=cluster_name,
                serviceName=service_name,
                taskDefinition=task_definition,
                desiredCount=1,
                launchType='FARGATE',
                networkConfiguration={
                       'awsvpcConfiguration': {
                       'subnets': [
                            response['Subnets'][0],
                            response['Subnets'][1],
                            ],
                       'securityGroups': [
                             response['Sec_groups'],
                             ],
                       'assignPublicIp': 'ENABLED'
                       }
                       },

                       )
# pprint.pprint(response3)

#time.sleep(10)
#create_service(cluster_name,service_name,task_defination)
#time.sleep(60)

def list_tasks(cluster_name,service_name):
         response = client.list_tasks(
             cluster=cluster_name,
             serviceName=service_name,
             desiredStatus='RUNNING',
             launchType='FARGATE'
         )
         pprint.pprint(response)
         task =response['taskArns']
         pprint.pprint(task)
         return task
#task_name=list_tasks(cluster_name,service_name)

def describe_tasks(task_name,cluster_name):
       task = task_name
       response4 = client.describe_tasks(
          cluster = cluster_name,
          tasks = [task[0]]
       )
       pprint.pprint(response4)
       enino = response4['tasks'][0]['attachments'][0]['details'][1]['value']
       pprint.pprint(enino)
       return enino
#interfaceid = describe_tasks(task_name,cluster_name)

def network_interface(interfaceid):
        network_interfaceid = interfaceid
        response5 = client1.describe_network_interfaces(

             NetworkInterfaceIds=[interfaceid],
        )
        pprint.pprint(response5)
        publicip = response5['NetworkInterfaces'][0]['Association']['PublicIp']
        pprint.pprint(publicip) 
        return publicip

 #network_interface(interfaceid)

def delete_service(cluster_name,service_name):
      response = client.delete_service(
        cluster=cluster_name,
        service=service_name,
        force=True  
      )
def delete_cluster(cluster_name):
        response = client.delete_cluster(
            cluster=cluster_name
        )  
#delete_cluster('test')
