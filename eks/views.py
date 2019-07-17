# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import EksInfo,EksTempInfo
from my_definitions import CreateStack
from my_definitions import DescribeStackoutputs
from my_definitions import createcluster
from my_definitions import DescribeCluster
from my_definitions import createstackworkernodes
from my_definitions import describe_workers_stack
from my_definitions import config
from my_definitions import get_externalip
from terminate import delete_cluster
from terminate import delete_stack
from django.contrib.auth.decorators import login_required

# Create your views here.
import boto3
import time
import os
import subprocess
import json
import yaml
import sys

data = []
cluster_details = {}

@login_required
def awseksconfirm(request):
        return render(request, 'eks/eks-form.html')

def awseksview(request):
    if request.method == 'POST':
	stack_name = request.POST.get('Stack_name', False)
        cluster_name = request.POST.get('EKSCluster',False)
        workers_stack_name = request.POST.get('Workers_stack_name',False)
        worker_nodes = request.POST.get('worker_nodes',False)
        repo_name = request.POST.get('repo_name', False)
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        image_name = request.POST.get('image_name', False)
        port = request.POST.get('port', False)
        target_port = request.POST.get('target_port', False)
        if os.path.exists("/home/ubuntu/venv/mmp/aws/jenkinslog.html"):
            os.remove("/home/ubuntu/venv/mmp/aws/jenkinslog.html")
        else:
            print("\njenkinslog.html does not exist")
        subprocess.call(['./cpkubeeksconfig'])
        #if os.path.exists("/home/ubuntu/venv/mmp/aws/eks/templates/eks/jenkinslog.html"):
        #    os.remove("/home/ubuntu/venv/mmp/aws/eks/templates/eks/jenkinslog.html")
        #else:
        #    print("\njenkinslog.html does not exist")
        print("\nThe Git Info is below")
        print(repo_name)
        print(username)
        print(password)
        print("\n")
        print(image_name)
        print(port)
        print(target_port)
        with open("/home/ubuntu/venv/mmp/aws/git-reponame.txt", "w") as f:
            f.write(repo_name)
        with open("/home/ubuntu/venv/mmp/aws/git-username.txt", "w") as f:
            f.write(username)
        with open("/home/ubuntu/venv/mmp/aws/git-password.txt", "w") as f:
            f.write(password)
        with open("/home/ubuntu/venv/mmp/aws/imagename.txt", "w") as f:
            f.write(image_name)
        with open("/home/ubuntu/venv/mmp/aws/port.txt", "w") as f:
            f.write(port)
        with open("/home/ubuntu/venv/mmp/aws/targetport.txt", "w") as f:
            f.write(target_port)
        dqote='"'
        top = "<html><head><title></title><head><body><textarea cols="+dqote+"157"+dqote+" wrap="+dqote+"hard"+dqote+">"
        breakrule = "<br><br>"
        bottom = "</textarea></body></html>"
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "w+") as f:
            f.write(top)
        eks = boto3.client('eks',region_name='us-west-2')
	ekstemp_refresh = EksTempInfo.objects.all()
	ekstemp_refresh.delete()
	ekstempinfo = EksTempInfo.objects.create(MasterStack=stack_name,EksClusterName=cluster_name,WorkersStack=workers_stack_name,WorkerNo=worker_nodes)
        cloudformation = boto3.client('cloudformation',region_name='us-west-2')
        stackmaster=CreateStack(cloudformation,stack_name)
        print("\nThe Stack creation is below")
        print stackmaster
        stackmaster1 = str(stackmaster)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(stackmaster1)
        time.sleep(120)
        outputs=DescribeStackoutputs(cloudformation,stack_name)
        print("\nThe Stack output is below")
        print outputs
        outputs1 = str(outputs)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(outputs1)
        cluster=createcluster(eks,outputs,cluster_name)
        time.sleep(660)
        clusterinfo=DescribeCluster(eks,cluster_name)
        print("\nThe clusterinfo is below")
        print clusterinfo
        clusterinfo1 = str(clusterinfo)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(clusterinfo1)
        workerstack=createstackworkernodes(cloudformation,workers_stack_name,outputs,worker_nodes,cluster_name)
        print("\nThe workerstack output is below")
        print workerstack
        workerstack1 = str(workerstack)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(workerstack1)
        time.sleep(240)
        workerstack_info=describe_workers_stack(cloudformation,workers_stack_name)
        print("\nThe workerstack_info is below")
        print workerstack_info
        workerstack_info1 = str(workerstack_info)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(workerstack_info1)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(breakrule)
        configuration=config(clusterinfo,cluster_name,workerstack_info)
        time.sleep(30)
        f = open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+")
        #subprocess.call(['./commands'], stdout=f)
        subprocess.call(['./docker-commands'], stdout=f)
        time.sleep(120)
        subprocess.call(['./monitoring'], stdout=f)
        time.sleep(120)
        with open("/home/ubuntu/venv/mmp/aws/jenkinslog.html", "a+") as f:
            f.write(bottom)
        time.sleep(30)
        #subprocess.call(['./runjenkins'])
        externalipfile = open("/home/ubuntu/venv/mmp/aws/docker-url.txt","r")
        externalipread = externalipfile.read()
        #externalip = externalipread+":8082/webapp"
        externalip = externalipread+"/cmdb"
        monitoringipfile = open("/home/ubuntu/venv/mmp/aws/grafana.txt","r")
        monitoringipread = monitoringipfile.read()
        monitoringip = monitoringipread+":3000"
        eksclusterinfo = EksInfo.objects.create(MasterStack=stack_name,EksClusterName=cluster_name,WorkersStack=workers_stack_name,WorkerNo=worker_nodes,ExternalIP=externalip,MonitoringIP=monitoringip)
        subprocess.call(['./rungrafana'])
        return HttpResponse(None)
    #else:
    #    return render(request, 'eks/eks-form.html')

def awseksredirect(request):
	clusters = EksTempInfo.objects.all()
        return render(request, 'eks/eks-info.html', {'clusters': clusters})

def table(request):
    clusters = EksInfo.objects.all()
    return render(request, 'eks/eks_formtable.html', {'clusters': clusters})

def logs(request):
    return render(request, 'eks/eks-logs.html')

def jenkinslog(request):
    return render(request, 'eks/jenkinslog.html')

def awseksterminate(request):
        cluster_name = request.POST.get('clustername',False)
	details = EksInfo.objects.get(EksClusterName=cluster_name)
        EksInfo.objects.filter(EksClusterName=cluster_name).delete()
	eks = boto3.client('eks',region_name='us-west-2')
        cloudformation = boto3.client('cloudformation',region_name='us-west-2')
        stack_name = details.MasterStack
        stack_name_workernodes = details.WorkersStack
	workerstacktermination = delete_stack(cloudformation,stack_name_workernodes)
        clusterdelete = delete_cluster(eks,cluster_name)
        masterstacktermination = delete_stack(cloudformation,stack_name)
        return HttpResponse(None)
        
def stacklist(request):
    if request.method == 'GET':
        stack_list=[]
        cloudformation = boto3.client('cloudformation', region_name='us-west-2',)
        response_list = cloudformation.list_stacks(
        )
        result=response_list['StackSummaries'][0]['StackName']
        #return HttpResponse(result)
        #return render(request, 'eks/eks-form.html', result)
        stack_list.append(dict(name=result))
        return HttpResponse(json.dumps(stack_list))

    else:
        return render(request, 'eks/eks-form.html')

def git_creds(request):
    if request.method == 'POST':
	repo_name = request.POST.get('repo_name', False)
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        print(repo_name)
        print(username)
        print(password)
        with open("/home/ubuntu/venv/mmp/aws/git-reponame.txt", "wb") as f:
            f.write(repo_name)
        with open("/home/ubuntu/venv/mmp/aws/git-username.txt", "wb") as f:
            f.write(username)
        with open("/home/ubuntu/venv/mmp/aws/git-password.txt", "wb") as f:
            f.write(password)
