# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-04 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrasetup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clusterinfo',
            name='MasterNo',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='clusterinfo',
            name='SlaveNo',
            field=models.PositiveIntegerField(),
        ),
    ]
