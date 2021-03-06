#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai.models import User


class UserSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    talent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_superuser', 'phone', 'talent', 'department', 'is_active',
                  'date_joined', 'last_login']

    def get_department(self, obj):
        department = obj.department.filter().first()
        return {'name': department.get_department_name(), 'id': department.id} if department else {'name': '', 'id': -1}

    def get_talent(self, obj):
        talent = obj.get_talent()
        return talent.get_talent_name() if talent else ''
