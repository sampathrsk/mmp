
# Create your views here.

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
 # -*- coding: utf-8 -*-

from definitions import create_cluster
from .models import AksInfo,AksTempInfo

# Create your views here.
import time
import os
import subprocess
import json
import yaml
import sys

import credentials

subscription_id = credentials.subscription_id
TenantID = credentials.tenant_id
ClientID = credentials.client_id
Secret = credentials.secret
print(subscription_id+"yahi hai")

#awseksprovision = False
def home(request):
    return render(request, 'form.html')
 
def data_view(request):
    if request.method == 'POST':
        #subscription_id = request.POST.get('subscription',False)
        #print(subscription_id)
        #TenantID = request.POST.get('tenant', False)
        #print(TenantID)
        #ClientID = request.POST.get('client',False)
        #print(ClientID)
        #Secret  = request.POST.get('secret', False)        
        private_key = request.POST.get('ssh_key', False)
        cluster_name = request.POST.get('AKSCluster', False)
        with open("/home/ubuntu/venv/mmp/aws/aksname.txt", "w") as f:
            f.write(cluster_name)
        resource_group_name = request.POST.get('resource_group', False)
        worker_nodes = request.POST.get('worker_nodes', False)
        print(worker_nodes)
        ftemp_refresh = AksTempInfo.objects.all()
        ftemp_refresh.delete()
        Ftempinfo = AksTempInfo.objects.create(AksClusterName=cluster_name,ResourceGroupName=resource_group_name,WorkerNo=worker_nodes)
        repo_name = request.POST.get('repo_name', False)
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        subprocess.call(['./mvkubeeksconfig'])
        print("\nThe Git Info is below")
        print(repo_name)
        print(username)
        print(password)
        with open("/home/ubuntu/venv/mmp/aws/git-reponame.txt", "w") as f:
            f.write(repo_name)
        with open("/home/ubuntu/venv/mmp/aws/git-username.txt", "w") as f:
            f.write(username)
        with open("/home/ubuntu/venv/mmp/aws/git-password.txt", "w") as f:
            f.write(password)
        cluster=create_cluster(subscription_id, TenantID, ClientID, Secret, cluster_name, resource_group_name, worker_nodes, private_key)
        print("\n\n")
        #print(cluster)
        #print(cluster['location'])
        #print(cluster['name'])
        #print(cluster['properties']['linuxProfile']['adminUsername'])
        #print(cluster['properties']['agentPoolProfiles'][0]['count'])
        time.sleep(240)
        subprocess.call(['./akscommands'])
        time.sleep(120)
        subprocess.call(['./azmonitoring'])
        time.sleep(120)
        externalipfile = open("/home/ubuntu/venv/mmp/aws/aztomcat.txt","r")
        externalipread = externalipfile.read()
        externalip = externalipread+":8082/webapp"
        monitoringipfile = open("/home/ubuntu/venv/mmp/aws/azgrafana.txt","r")
        monitoringipread = monitoringipfile.read()
        monitoringip = monitoringipread+":3000"
        fclusterinfo = AksInfo.objects.create(AksClusterName=cluster_name,ResourceGroupName=resource_group_name,WorkerNo=worker_nodes,ExternalIP=externalip,MonitoringIP=monitoringip)
        subprocess.call(['./azrungrafana'])
        return HttpResponse(None)
        

def temp_details(request):
    
    return render(request, 'temp.html')

def redirect(request):
    clusters = AksTempInfo.objects.all()
    return render(request, 'atable.html', {'clusters': clusters})

def ftable(request):
    clusters = AksInfo.objects.all()
    return render(request, 'formtable.html', {'clusters': clusters})

def azureaksterminate(request):
        cluster_name = request.POST.get('AKSCluster', False)
	details = AksInfo.objects.get(AksClusterName=cluster_name)
        AksInfo.objects.filter(AksClusterName=cluster_name).delete()
        return HttpResponse(None)

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
