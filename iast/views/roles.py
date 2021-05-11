#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/10 下午2:26
# project: dongtai-webapi
from django.contrib.auth.models import Group
from dongtai_models.models.group_routes import AuthGroupRoutes

from base import R
from iast.base.user import TalentAdminEndPoint
from iast.serializers.routes import RouteSerializer


class RolesEndPoint(TalentAdminEndPoint):
    def get(self, request):
        queryset = AuthGroupRoutes.objects.filter(created_by=request.user)
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)

        try:
            page_summary, queryset = self.get_paginator(queryset, page, page_size)

            return R.success(data={"data": RouteSerializer(queryset, many=True).data,
                                   "page": page_summary,
                                   "total": page_summary['alltotal']})
        except ValueError as e:
            return R.failure(msg='page和pageSize必须是数字')

    def post(self, request, role_id):
        is_active = request.data.get('isActive')
        routes = request.data.get('menuKeys')
        try:
            import time
            timestamp = int(time.time())
            group_route = AuthGroupRoutes.objects.filter(id=role_id, created_by=request.user).first()
            if group_route:
                group_route.routes = routes
                group_route.update_time = timestamp
                group_route.is_active = is_active
                group_route.save(update_fields=['routes', 'update_time', 'is_active'])
                return R.success(msg=f'修改成功')
            else:
                return R.failure(msg=f'角色不存在')
        except Exception as e:
            print(e)
        return R.failure(msg=f'修改失败')

    def delete(self, request, role_id):
        try:
            group_route = AuthGroupRoutes.objects.get(id=role_id, created_by=request.user)
            group = group_route.group
            if group.user_set.count() > 0:
                return R.failure(msg='该角色下存在用户，请先修改用户角色或删除用户，再删除该角色')
            role_name = group.name
            group_route.delete()
            group.delete()
            return R.success(msg=f'角色{role_name}删除成功')
        except Exception as e:
            return R.failure(msg='角色id不存在')

    def put(self, request):
        role_name = request.data.get('roleName')
        is_active = request.data.get('isActive')
        routes = request.data.get('menuKeys')
        try:
            import time
            timestamp = int(time.time())
            group = Group.objects.create(name=role_name)
            AuthGroupRoutes.objects.create(
                routes=routes,
                group=group,
                created_by=request.user,
                create_time=timestamp,
                update_time=timestamp,
                is_active=is_active
            )
            return R.success(msg=f'角色：{role_name}  创建成功')
        except Exception as e:
            pass
        return R.failure(msg=f'角色：{role_name}  创建成功')
