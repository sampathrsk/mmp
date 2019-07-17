# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class EcsInfo(models.Model):
    ClusterName = models.CharField(max_length=30)
    TaskDefinitionName = models.CharField(max_length=30)
    ServiceName = models.CharField(max_length=30)
    ContainerName = models.CharField(max_length=30)
    PublicIp = models.CharField(max_length=30)



class EcsTempInfo(models.Model):
        Clustername = models.CharField(max_length=30)
        TaskDefinitionName = models.CharField(max_length=30)
        ServiceName = models.CharField(max_length=30)
        ContainerName = models.CharField(max_length=30)
        PublicIp = models.CharField(max_length=30)

