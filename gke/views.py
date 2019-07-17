# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-

from .models import GkeInfo,GkeTempInfo
from my_definitions import gke_create_cluster
from django.contrib.auth.decorators import login_required

from google.cloud import container_v1
client = container_v1.ClusterManagerClient()

# Create your views here.
import time
import subprocess

data = []
cluster_details = {}

@login_required
def gkeconfirm(request):
    return render(request, 'gke/gke-form.html')

def gkeredirect(request):
    clusters = GkeTempInfo.objects.all()
    return render(request, 'gke/gke-info.html', {'clusters': clusters})

def gkeexecute(request):
    if request.method == 'POST':
        project_id = 'laasprobhu'
        zone = 'us-central1-a'
        cluster_name = request.POST.get('Cluster_name', False)
        nodes = request.POST.get('Nodes', False)
        nodes = nodes.encode("utf8")
        nodes = int(nodes)
        disksize = request.POST.get('Disk_size', False)
        disksize = int(disksize)
        gkeclusterinfo = GkeInfo.objects.create(GkeClusterName=cluster_name,ProjectId=project_id,Zone=zone,Nodes=nodes)
        gketemp_refresh = GkeTempInfo.objects.all()
        gketemp_refresh.delete()
        gketempinfo = GkeTempInfo.objects.create(GkeClusterName=cluster_name,ProjectId=project_id,Nodes=nodes,DiskSize=disksize)
        cluster = gke_create_cluster(cluster_name,nodes,disksize)
        response = client.create_cluster(project_id, zone, cluster)
        time.sleep(240)
        subprocess.call(['./gkecommands'])
        print response

def gketable(request):
    clusters = GkeInfo.objects.all()
    return render(request, 'gke/gke_formtable.html', {'clusters': clusters})

def gketerminate(request):
    project_id = 'laasprobhu'
    zone = 'us-central1-a'
    cluster_name = request.POST.get('clustername',False)
    print cluster_name
    GkeInfo.objects.filter(GkeClusterName=cluster_name).delete()
    response = client.delete_cluster(project_id, zone, cluster_name)


