# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import FgInfo,FgTempInfo
from fg_definitions import *
from vpc import *
from django.contrib.auth.decorators import login_required

# Create your views here.
import boto3
import time
import os
import subprocess
import json
import yaml

reg='ap-southeast-1'
ec2 = boto3.resource('ec2', region_name=reg)

data = []
cluster_details = {}

@login_required
def awsfgconfirm(request):
        return render(request, 'fg-form.html')

def awsfgview(request):
    if request.method == 'POST':
	cluster_name = request.POST.get('cluster_name',False)
        print(cluster_name)
        task_def_name = request.POST.get('task_def_name',False)
        print(task_def_name)
        container_name = request.POST.get('container_name',False)
        print(container_name)
        service_name = request.POST.get('fg_name',False)
        print(service_name)
        create_cluster(cluster_name)
        task_definition = register_task_definition(task_def_name,container_name)
        pprint.pprint(task_definition)
        vpcname='fargate_vpc'
        sg_subnet=create_fargate_vpc(vpcname,ec2)
        create_service(cluster_name,service_name,task_definition,sg_subnet)
        time.sleep(40)
        task_name = list_tasks(cluster_name,service_name)
        interfaceid = describe_tasks(task_name,cluster_name) 
        publicip = network_interface(interfaceid)
        fgclusterinfo = FgInfo.objects.create(ClusterName=cluster_name,TaskDefinitionName=task_def_name,ContainerName=container_name,ServiceName=service_name,PublicIp=publicip)
        fgtemp_refresh = FgTempInfo.objects.all()
        fgtemp_refresh.delete()
        Fgtempinfo = FgTempInfo.objects.create(Clustername=cluster_name,TaskDefinitionName=task_def_name,ContainerName=container_name,ServiceName=service_name,PublicIp=publicip)

    #else:
    #    return render(request, 'eks/eks-form.html')

def awsfgredirect(request):
	clusters = FgTempInfo.objects.all()
        return render(request, 'fg-info.html', {'clusters': clusters})

def table(request):
    clusters = FgInfo.objects.all()
    return render(request, 'fg_formtable.html', {'clusters': clusters})

def awsfgterminate(request):
	  print(request.POST)
          clustername = request.POST.get('clustername',False)
          pprint.pprint(clustername) 
	  servicename = request.POST.get('fgname',False)
          pprint.pprint(servicename)
          details = FgInfo.objects.get(ClusterName=clustername)
          pprint.pprint(details)
          FgInfo.objects.filter(ClusterName=clustername).delete()
	  fg = boto3.client('ecs',region_name='ap-southeast-1')
          delete_service(clustername,servicename)
          delete_cluster(clustername)

        
        #cloudformation = boto3.client('cloudformation',region_name='us-west-2')
        #stack_name = details.MainStack
        #stack_name_workernodes = details.WorkersStack
	#workerstacktermination = delete_stack(cloudformation,stack_name_workernodes)
        #clusterdelete = delete_cluster(eks,cluster_name)
        #mainstacktermination = delete_stack(cloudformation,stack_name)
        

