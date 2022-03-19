#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai.models.agent import IastAgent
from dongtai.utils.settings import get_managed


class IastErrorlog(models.Model):
    errorlog = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_errorlog'
