######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route
# @created     : Tuesday Aug 17, 2021 17:43:27 CST
#
# @description :
######################################################################

from django.db import models
from dongtai.utils.settings import get_managed
from dongtai.models.agent import IastAgent


class HttpMethod(models.Model):
    method = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_http_method'


class IastApiMethod(models.Model):
    method = models.CharField(max_length=100, blank=True)
    http_method = models.ManyToManyField(
        HttpMethod, blank=True, through='IastApiMethodHttpMethodRelation')

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_methods'


class IastApiMethodHttpMethodRelation(models.Model):
    api_method = models.ForeignKey(IastApiMethod,
                                   on_delete=models.CASCADE,
                                   db_constraint=False,
                                   db_column='api_method_id')
    http_method = models.ForeignKey(HttpMethod,
                                    on_delete=models.CASCADE,
                                    db_constraint=False,
                                    db_column='http_method_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_http_method_relation'
        unique_together = ['api_method_id', 'http_method_id']


class IastApiRoute(models.Model):
    path = models.CharField(max_length=255, blank=True)
    code_class = models.CharField(max_length=255,
                                  blank=True,
                                  db_column='code_class')
    description = models.CharField(max_length=500, blank=True)
    method = models.ForeignKey(IastApiMethod,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               db_index=True,
                               db_column='method_id')
    code_file = models.CharField(max_length=500,
                                 blank=True,
                                 db_column='code_file')
    controller = models.CharField(max_length=100, blank=True)
    agent = models.ForeignKey(IastAgent,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='agent_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_route'
        unique_together = ['path', 'method']


class IastApiParameter(models.Model):
    name = models.CharField(max_length=100, blank=True)
    parameter_type = models.CharField(max_length=100,
                                      blank=True,
                                      db_column='type')
    annotation = models.CharField(max_length=500, blank=True)
    route = models.ForeignKey(IastApiRoute,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='route_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_parameter'
        unique_together = ['name', 'route_id']


class IastApiResponse(models.Model):
    return_type = models.CharField(max_length=100, blank=True)
    route = models.ForeignKey(IastApiRoute,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='route_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_response'
        unique_together = ['return_type', 'route_id']
