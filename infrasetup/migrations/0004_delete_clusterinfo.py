# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-28 05:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infrasetup', '0003_clusterdetails_new'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClusterInfo',
        ),
    ]