#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/24 下午9:07
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.auth import authenticate

from base import R
from iast.base.user import UserEndPoint
from webapi import settings


class UserPassword(UserEndPoint):
    name = "api-v1-user-password"
    description = "修改密码"

    def post(self, request):
        user = request.user
        # edit by song 校验旧密码
        if not request.data['old_password'] or not request.data['new_password'] or self.invalid_password(
                request.data['new_password']):
            return R.failure(msg='旧密码为空或新密码格式不正确，正确格式：6-20位，必须包含字母、数字、特殊符号的两种以上')
        else:
            user_check = authenticate(username=user.username, password=request.data['old_password'])
            if user_check is not None and user_check.is_active:
                password = request.data['new_password']

                user.set_password(password)
                user.save(update_fields=['password'])
                self.modify_atom_password(username=user.username, password=request.data['new_password'],
                                          old_password=request.data['old_password'],
                                          access_token=request.META['HTTP_X_ACCESS_TOKEN'])

                return R.success(msg='密码修改成功')
            else:
                return R.failure(msg='原始密码错误')

    @staticmethod
    def modify_atom_password(username, password, old_password, access_token):
        try:
            import requests
            body = {
                'username': username,
                'password': password,
                'oldPassword': old_password,
                'verifyPassword': password
            }
            headers = {
                'x-access-token': access_token
            }
            resp = requests.post(url=settings.ATOM_HOST + "/v1/user/modifypwd", data=body, headers=headers, verify=False)
            print(resp.text)
            return True
        except:
            return False

    @staticmethod
    def invalid_password(password):
        """
        验证密码格式是否正确
        """
        import re
        rule = '^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$).{6,20}$'
        if password and password != '' and len(password) >= 6 and re.findall(rule, password):
            return False
        return True
