#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/10 下午3:14
# project: dongtai-webapi
from dongtai_models.models.group_routes import AuthGroupRoutes

from base import R
from iast.base.user import UserEndPoint


class RouteEndPoint(UserEndPoint):
    def get(self, request):
        route = AuthGroupRoutes.objects.values('routes').filter(group=request.user.groups.first(), is_active=1).first()
        if route:
            return R.success(data=route['routes'])
        else:
            return R.failure(msg='当前用户所属的用户角色不存在或已被禁用')
