######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : demo
# @created     : Wednesday Aug 04, 2021 15:00:46 CST
#
# @description :
######################################################################

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.user import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.conf import settings
from iast.utils import parse_x_host, get_domain_from_x_host
from urllib.parse import urljoin
from webapi.settings import CSRF_COOKIE_NAME

class Demo(UserEndPoint):
    permission_classes = []
    authentication_classes = []
    name = "user_views_login"
    description = "用户登录"

    def get(self, request):
        user = User.objects.filter(username="demo").first()
        login(request, user)
        host = parse_x_host(request)
        base_url = get_domain_from_x_host(request)
        if base_url:
            host = parse_x_host(request)
            res = HttpResponseRedirect(
                urljoin(base_url, "project/projectManage"))
            res.set_cookie('sessionid', domain=host)
            res.set_cookie(CSRF_COOKIE_NAME, domain=host)
            return res
        else:
            res = HttpResponseRedirect(settings.DOMAIN + "project/projectManage")
        return res
