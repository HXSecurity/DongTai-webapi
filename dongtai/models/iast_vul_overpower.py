#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/31 11:38
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai.models.agent import IastAgent

from dongtai.utils.settings import get_managed


class IastVulOverpower(models.Model):
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    http_url = models.CharField(max_length=2000, blank=True, null=True)
    http_uri = models.CharField(max_length=2000, blank=True, null=True)
    http_query_string = models.CharField(max_length=2000, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    http_scheme = models.CharField(max_length=255, blank=True, null=True)
    http_protocol = models.CharField(max_length=255, blank=True, null=True)
    http_header = models.CharField(max_length=2000, blank=True, null=True)
    x_trace_id = models.CharField(max_length=255, blank=True, null=True)
    cookie = models.CharField(max_length=2000, blank=True, null=True)
    sql = models.CharField(max_length=2000, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_vul_overpower'
