#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/14 下午4:13
# project: dongtai-webapi
from django.contrib.auth.models import Group

from base import R
from iast.base.user import TalentAdminEndPoint
from iast.serializers.rolename import RoleNameSerializer


class RoleNameEndPoint(TalentAdminEndPoint):
    def get(self, request):
        queryset = Group.objects.all()
        return R.success(data=RoleNameSerializer(queryset, many=True).data)
