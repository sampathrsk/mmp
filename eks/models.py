# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class EksInfo(models.Model):
    MasterStack = models.CharField(max_length=230)
    EksClusterName = models.CharField(max_length=230)
    WorkersStack = models.CharField(max_length=230)
    WorkerNo = models.CharField(max_length=230)
    ExternalIP = models.CharField(max_length=290, null=True, blank=True)
    MonitoringIP = models.CharField(max_length=290, null=True, blank=True)

class EksTempInfo(models.Model):
        MasterStack = models.CharField(max_length=230)
        EksClusterName = models.CharField(max_length=230)
        WorkersStack = models.CharField(max_length=230)
        WorkerNo = models.CharField(max_length=230)
