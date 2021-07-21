#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/5 上午10:44
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from import_export import resources
from rest_framework.generics import GenericAPIView

from dongtai.endpoint import R


class LogResurce(resources.ModelResource):
    def get_export_headers(self):
        return [
            u'时间', u'用户', u'操作记录'
        ]

    class Meta:
        model = LogEntry
        fields = ('user', 'action_time', 'change_message')


class ExportMixin(object):
    @staticmethod
    def attachment_response(export_data, filename='download.xls', content_type='application/vnd.ms-excel'):
        """
        日志导出中文名乱码问题解决方案：
        - https://segmentfault.com/q/1010000009719860
        - https://blog.csdn.net/qq_34309753/article/details/99628474

        :param export_data:
        :param filename:
        :param content_type:
        :return:
        """
        response = HttpResponse(export_data, content_type=content_type)
        response['content_type'] = content_type
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        return response

    def get(self, request):
        ids = request.query_params.get('ids')
        if ids:
            ids = [int(id.strip()) for id in ids.split(',')]
            user = request.user
            if user.is_talent_admin():
                queryset = LogEntry.objects.filter(id__in=ids).filter()
            else:
                queryset = LogEntry.objects.filter(id__in=ids, user=user).filter()

            resources = self.resource_class()
            export_data = resources.export(queryset, False)
            return ExportMixin.attachment_response(getattr(export_data, 'xls'), filename='用户操作日志.xls')
        else:
            return R.failure(status=202, msg='导出失败，原因：日志ID不能为空')


class LogExport(ExportMixin, GenericAPIView):
    resource_class = LogResurce
