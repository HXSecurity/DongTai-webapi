# Create your views here.

from dongtai.endpoint import UserEndPoint
from dongtai.endpoint import R
from dongtai.endpoint import AnonymousAndUserEndPoint
from django.utils.translation import gettext_lazy as _
import json
import logging
from license.license_encrypt import license_validate, get_license_detail, getmachineid
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from dongtai.models.agent import IastAgent
from dongtai.utils import const
from license.utils import get_license, get_agent_concurrency, store_license, delete_license, url_validate
from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import render, HttpResponse

from rest_framework import status
from django.http import JsonResponse

logger = logging.getLogger("dongtai-webapi")


class UploadLicenseSerializer(serializers.Serializer):
    license = serializers.CharField()


class UploadLicense(UserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')],
                                 request=UploadLicenseSerializer)
    def post(self, request):
        license = request.data.get('license', None)
        result = license_validate(license)
        if result is False:
            return R.failure(msg='license error')
        store_license(license)
        return R.success()


class DetailLicense(UserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')])
    def get(self, request):
        license_data = get_license_detail(get_license())
        return R.success(data=license_data)


class DeleteLicense(UserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')])
    def get(self, request):
        delete_license()
        return R.success()


class CurrentConcurrency(UserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')])
    def get(self, request):
        res = IastAgent.objects.filter(online=const.RUNNING).count()
        return R.success(data=res)


class ShowMachineCode(UserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')])
    def get(self, request):
        return R.success(data=getmachineid().decode('utf-8'))


class IsAuthenticated(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(tags=[_('License')])
    def get(self, request):
        result = license_validate(get_license())
        return R.success(data=result)




class LicenseCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        if license_validate(get_license()) or url_validate(request.path):
            return None
        else:
            content = {'msg': _('The system is not authorized')}
            return JsonResponse(content,
                                status=status.HTTP_402_PAYMENT_REQUIRED)




