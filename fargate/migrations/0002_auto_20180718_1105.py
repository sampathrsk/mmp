# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-18 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fargate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FgTempInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Clustername', models.CharField(max_length=30)),
                ('TaskDefinitionName', models.CharField(max_length=30)),
                ('ServiceName', models.CharField(max_length=30)),
                ('ContainerName', models.CharField(max_length=30)),
                ('PublicIp', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='fginfo',
            name='PublicIp',
            field=models.CharField(max_length=30),
        ),
    ]