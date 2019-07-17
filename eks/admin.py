# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EksInfo, EksTempInfo

# Register your models here.
admin.site.register(EksInfo)
admin.site.register(EksTempInfo)