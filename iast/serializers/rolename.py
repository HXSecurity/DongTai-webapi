#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/14 下午4:16
# project: dongtai-webapi
from django.contrib.auth.models import Group
from rest_framework import serializers


class RoleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
