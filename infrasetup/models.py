# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class clusterdetails_new(models.Model):
    clustername = models.CharField(max_length=40)
    region = models.CharField(max_length=40)
    masterno = models.PositiveIntegerField()
    instatypem = models.CharField(max_length=30)
    slaveno = models.PositiveIntegerField()
    instatypes = models.CharField(max_length=30)
    masterasg = models.CharField(max_length=40)
    slaveasg = models.CharField(max_length=40)