# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class AksInfo(models.Model):
    AksClusterName = models.CharField(max_length=30)
    ResourceGroupName = models.CharField(max_length=30)
    WorkerNo = models.CharField(max_length=30)
    ExternalIP = models.CharField(max_length=290, null=True, blank=True)
    MonitoringIP = models.CharField(max_length=290, null=True, blank=True)

class AksTempInfo(models.Model):
	AksClusterName = models.CharField(max_length=30)
	ResourceGroupName = models.CharField(max_length=30)
	WorkerNo = models.CharField(max_length=30)
