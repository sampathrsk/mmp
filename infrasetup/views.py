# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

#from django.shortcuts import render

# Create your views here.
 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import awsform
from django.http import JsonResponse
from datetime import datetime
from .models import clusterdetails_new
from django.contrib.auth.decorators import login_required

import boto3
import time
import terminate
# Create your views here.
data=['a']

def infoview(request):
	return render(request, 'infrasetup/form1.html')

def VpcLaunch(request):
	region = request.GET.get('region', None)
        if region!='':
		ec2 = boto3.resource('ec2', region_name = region)
		autoscaling = boto3.client('autoscaling',region_name = region)
		#print ec2,autoscaling
		from my_definitions import describe_vpcs
		vpc = describe_vpcs(ec2)
		from my_definitions import describe_autoscaling_launchconfigurations
		launch_config = describe_autoscaling_launchconfigurations(autoscaling)
	else:
		vpc = '';
		launch_config = '';

#		return render(request,'infrasetup/vpcList.html',{'vpc':vpc})
	return JsonResponse({'vpc':vpc , 'launch_config':launch_config})


def clusternamecheck(request):
	region = request.GET.get('region', None)
	name = request.GET.get('name', None)
	if name!='':
		#print name
		from my_definitions import fetchclustername
		details = fetchclustername(region)
		if details['length'] == 0:
			Noclusters = True
		else:
			if any(i in name for i in details['x'][0]):
				Noclusters = False
			else:
				Noclusters = True
	else:
		Noclusters = False

	#print Noclusters
		
	return JsonResponse({'clusternamecheck': Noclusters})
	
def mainasgnamecheck(request):
        region = request.GET.get('region', None)
        name = request.GET.get('name', None)
        if name!='':
                #print name
                from my_definitions import fetchclustername
                details = fetchclustername(region)
                if details['length'] == 0:
                        Nomainasg = True
                else:
                        if any(i in name for i in details['z']):
                                Nomainasg = False
                        else:
                                Nomainasg = True
        else:
                Nomainasg = False

        #print Nomainasg

        return JsonResponse({'mainasgnamecheck': Nomainasg})

def subordinateasgnamecheck(request):
        region = request.GET.get('region', None)
        name = request.GET.get('name', None)
        if name!='':
                #print name
                from my_definitions import fetchclustername
                details = fetchclustername(region)
                if details['length'] == 0:
                        Nosubordinateasg = True
                else:
                        if any(i in name for i in details['z']):
                                Nosubordinateasg = False
                        else:
                                Nosubordinateasg = True
        else:
                Nosubordinateasg = False

        #print Nosubordinateasg

        return JsonResponse({'subordinateasgnamecheck': Nosubordinateasg})


@login_required
def awsview(request):
  if request.method == 'POST' and request.POST.get('action') == 'Submit':
    form=awsform(request.POST)
    if form.is_valid():
      clustername = request.POST.__getitem__('Cluster_name')
      print clustername
      reg = form.cleaned_data['region']
      print reg
      vpc = form.cleaned_data['vpc']
      print vpc
      MainASG = request.POST.__getitem__('MainASG')
      #print MainASG
      launch_config = form.cleaned_data['launch_config']
      #print launch_config
      SubordinateASG = request.POST.__getitem__('SubordinateASG')
      #print SubordinateASG
      instancetypeM=form.cleaned_data['itypeM']
      #print instancetypeM
      instancetypeS=form.cleaned_data['itypeS']
      #print instancetypeS
      ver=form.cleaned_data['version']
      #print ver
      main=int(request.POST.__getitem__('main_nodes'))
      subordinate=int(request.POST.__getitem__('subordinate_nodes'))
      ec2 = boto3.resource('ec2', region_name = reg)
      client = boto3.client('ec2', region_name = reg)
      elb = boto3.client('elb', region_name = reg)
      autoscaling = boto3.client('autoscaling', region_name = reg)
      from provisioning_default import instance_provisioning
      #from terminate0 import instance_termination
      instance_provisioning(reg,vpc,ver,instancetypeM,ec2,client,elb,autoscaling,launch_config,main,'main',MainASG)
      instance_provisioning(reg,vpc,ver,instancetypeS,ec2,client,elb,autoscaling,launch_config,subordinate,'subordinate',SubordinateASG)
      startTime = datetime.now()
      #clusterdetails = Storedetailsindatabase(clustername,reg,main,instancetypeM,subordinate,instancetypeS,MainASG,SubordinateASG)
      clusterdetails = clusterdetails_new.objects.create(clustername=clustername,region=reg,mainno=main,instatypem=instancetypeM,subordinateno=subordinate,instatypes=instancetypeS,mainasg=MainASG,subordinateasg=SubordinateASG)
      time.sleep(25)
      describeinstances = autoscaling.describe_auto_scaling_instances()
      length = len(describeinstances['AutoScalingInstances'])
      print length
      ip = []
      AutoScalingGroupName = []
      def passglobalvariables(x,y):
          global data
          data.append(x)
          data.append(y)
      passglobalvariables(length,length)
      instances = {}
      for i in range(0,length):
          instanceid_i = describeinstances['AutoScalingInstances'][i]['InstanceId']
          AutoScalingGroupName_i = describeinstances['AutoScalingInstances'][i]['AutoScalingGroupName']
          ips = client.describe_instances(InstanceIds=[instanceid_i])
	  ip_i = ips['Reservations'][0]['Instances'][0]['PublicIpAddress']
	  ip.append(ip_i)
          AutoScalingGroupName.append(AutoScalingGroupName_i)
          passglobalvariables(ip_i,AutoScalingGroupName_i)
	  contexttemp = {}
	  contexttemp['InstanceIp'] = ip_i
	  contexttemp['AutoScalingGroupName']= AutoScalingGroupName_i
	  instances['Instance_%s'%i] = contexttemp
  
      print instances
      return render(request, 'infrasetup/results.html',{'instances':instances})
  else:
     form=awsform()
     return render(request, 'infrasetup/form.html' ,{'form':form})
 
def clustertable(request):
        clusters=clusterdetails_new.objects.all()
        return render(request, 'infrasetup/cluster-details.html',{'clusters': clusters})

def clusterterminate(request):
        cluster_name = request.POST.get('clustername',False)
        details = clusterdetails_new.objects.get(clustername=cluster_name)
        mainasg = details.mainasg
        print mainasg
        subordinateasg = details.subordinateasg
        reg = details.region
        ec2 = boto3.resource('ec2', region_name = reg)
	client = boto3.client('ec2', region_name = reg)
	elb = boto3.client('elb', region_name = reg)
	autoscaling = boto3.client('autoscaling', region_name = reg)
	terminatecluster = terminate.cluster_termination(reg,ec2,client,elb,autoscaling,mainasg,subordinateasg)
        clusterdetails_new.objects.filter(clustername=cluster_name).delete()

def guestbook(request):
	return render(request, 'infrasetup/guestbook.html')

def select(request):
	form=awsform(request.POST)
	a = request.POST.get('dropdown')
	print(a)
	if a == "baremetal":
		return render(request, 'infrasetup/form.html' ,{'form':form})
	elif a == "aws":
		return render(request, 'infrasetup/eks-form.html')

	elif a == "azure":
                return render(request, 'infrasetup/form.html')
	elif a == "google":
                return render(request, 'infrasetup/gke-form.html')
	print(a) 
