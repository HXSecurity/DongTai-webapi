#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午2:54
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai.utils.settings import get_managed

from dongtai.models.agent import IastAgent


class IastAgentProperties(models.Model):
    hook_type = models.IntegerField(blank=True, null=True)
    dump_class = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_properties'
