######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : details_id
# @created     : 星期一 12月 27, 2021 16:32:12 CST
#
# @description :
######################################################################



import logging

from dongtai.endpoint import UserEndPoint, R

from dongtai.utils import const
from iast.serializers.agent import AgentSerializer
from iast.serializers.project import ProjectSerializer
from iast.serializers.sca import ScaSerializer
from iast.serializers.vul import VulSerializer
from dongtai.models.asset import Asset
from iast.utils import get_model_field
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from functools import reduce
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai.models.vulnerablity import IastVulnerabilityModel


class IdsSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class DetailListWithid(UserEndPoint):
    serializers = serializers.Serializer
    def parse_ids(self, request):
        ser = IdsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                ids = ser.validated_data['ids']
        except ValidationError as e:
            return R.failure(data=e.detail)
        return ids

    def query(self, ids, request):
        return []

    def get(self, request):
        res = self.parse_ids(request)
        if not isinstance(res, list):
            return res
        ids = res
        items = self.query(ids, request)
        return R.success(data=self.serializer(items, many=True).data)


class AgentListWithid(DetailListWithid):
    serializer = AgentSerializer

    def query(self, ids, request):
        agents = IastAgent.objects.filter(pk__in=ids,
                                          user__in=self.get_auth_users(
                                              request.user)).all()
        return agents
    @extend_schema_with_envcheck(
        request=IdsSerializer,
        tags=[_('Agent')],
        summary=_('Agent List with id'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self, request):
        return super().get(request)


class ProjectListWithid(DetailListWithid):
    serializer = ProjectSerializer

    def query(self, ids, request):
        projects = IastProject.objects.filter(pk__in=ids,
                                              user__in=self.get_auth_users(
                                                  request.user)).all()
        return projects

    @extend_schema_with_envcheck(
        request=IdsSerializer,
        tags=[_('Project')],
        summary=_('Project List with id'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self, request):
        return super().get(request)


class ScaListWithid(DetailListWithid):
    serializer = ScaSerializer

    def query(self, ids, request):
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        scas = Asset.objects.filter(pk__in=ids, agent__in=auth_agents).all()
        return scas

    @extend_schema_with_envcheck(
        request=IdsSerializer,
        tags=[_('Component')],
        summary=_('Component List with id'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self, request):
        return super().get(request)


class VulsListWithid(DetailListWithid):
    serializer = VulSerializer

    def query(self, ids, request):
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        vuls = IastVulnerabilityModel.objects.filter(
            pk__in=ids, agent__in=auth_agents).values().all()
        return vuls

    @extend_schema_with_envcheck(
        request=IdsSerializer,
        tags=[_('Vulnerability')],
        summary=_('Vulnerability List with id'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self, request):
        return super().get(request)
