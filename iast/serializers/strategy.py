#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai.models.strategy import IastStrategyModel


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = IastStrategyModel
        fields = ['id', 'vul_type','vul_fix', 'level_id', 'state', 'vul_name', 'vul_desc', 'dt']
