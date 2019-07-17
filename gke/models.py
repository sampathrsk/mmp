# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class GkeInfo(models.Model):
    GkeClusterName = models.CharField(max_length=30)
    ProjectId = models.CharField(max_length=40)
    Zone = models.CharField(max_length=30)
    Nodes = models.CharField(max_length=30)

class GkeTempInfo(models.Model):
    GkeClusterName = models.CharField(max_length=30)
    ProjectId = models.CharField(max_length=30)
    Nodes = models.CharField(max_length=30)
    DiskSize = models.CharField(max_length=30)