# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class clusterdetails_new(models.Model):
    clustername = models.CharField(max_length=40)
    region = models.CharField(max_length=40)
    mainno = models.PositiveIntegerField()
    instatypem = models.CharField(max_length=30)
    subordinateno = models.PositiveIntegerField()
    instatypes = models.CharField(max_length=30)
    mainasg = models.CharField(max_length=40)
    subordinateasg = models.CharField(max_length=40)