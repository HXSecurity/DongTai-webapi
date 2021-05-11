#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/10 下午2:33
# project: dongtai-webapi
from dongtai_models.models.group_routes import AuthGroupRoutes
from rest_framework import serializers


class RouteSerializer(serializers.ModelSerializer):
    created_user = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = AuthGroupRoutes
        fields = ['id', 'created_user', 'create_time', 'update_time', 'role_name', 'routes', 'is_active']

    def get_role_name(self, obj):
        return obj.group.name

    def get_created_user(self, obj):
        return obj.created_by.get_full_name()
