######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_search
# @created     : Wednesday Aug 18, 2021 14:31:17 CST
#
# @description :
######################################################################

from django.db.models import Q
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.api_route import IastApiRoute, IastApiMethod, IastApiRoute, HttpMethod, IastApiResponse, IastApiMethodHttpMethodRelation, IastApiParameter
from dongtai.models.agent import IastAgent
from iast.base.project_version import get_project_version, get_project_version_by_id
from dongtai.models.vulnerablity import IastVulnerabilityModel
import hashlib
from dongtai.models.agent_method_pool import MethodPool
from django.forms.models import model_to_dict
from iast.utils import checkcover, batch_queryset
from django.core.cache import caches
from functools import partial
from dongtai.models.hook_type import HookType

class ApiRouteSearch(UserEndPoint):
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 1))
        page_index = int(request.query_params.get('page_index', 1))
        uri = request.query_params.get('uri', None)
        http_method = request.query_params.get('http_method', None)
        project_id = request.query_params.get('project_id', None)
        version_id = request.query_params.get('version_id', None)
        exclude_id = request.query_params.get('exclude_ids', None)
        exclude_id = [int(i)
                      for i in exclude_id.split(',')] if exclude_id else None
        is_cover = request.query_params.get('is_cover', None)
        is_cover_dict = {1: True, 0: False}
        is_cover = is_cover_dict[int(is_cover)] if is_cover is not None and is_cover != '' else None
        auth_users = self.get_auth_users(request.user)

        if http_method:
            http_method_obj = HttpMethod.objects.filter(method=http_method.upper())[0:1]
            if http_method_obj:
                api_methods = IastApiMethod.objects.filter(
                    http_method__id=http_method_obj[0].id).all().values('id')
        else:
            api_methods = []

        if not version_id:
            current_project_version = get_project_version(
                project_id, auth_users)
        else:
            current_project_version = get_project_version_by_id(version_id)
        agents = IastAgent.objects.filter(
            user__in=auth_users,
            bind_project_id=project_id,
            project_version_id=current_project_version.get("version_id",
                                                           0)).values("id")
        q = Q(agent_id__in=[_['id'] for _ in agents])
        q = q & Q(
            method_id__in=[_['id']
                           for _ in api_methods]) if api_methods != [] else q
        q = q & Q(path__icontains=uri) if uri else q
        q = q & ~Q(pk__in=exclude_id) if exclude_id else q
        api_routes = IastApiRoute.objects.filter(q).order_by('id').all()
        distinct_fields = ["path", "method_id"]
        distinct_exist_list = [] if not exclude_id else list(
            set([
                distinct_key(
                    IastApiRoute.objects.filter(pk=i).values(
                        "path", "method_id").first(), distinct_fields)
                for i in exclude_id
            ]))
        _filter_and_label_partial = partial(
            _filter_and_label,
            distinct=True,
            distinct_fields=distinct_fields,
            distinct_exist_list=distinct_exist_list)
        api_routes = _filter_and_label_partial(
            api_routes, page_size, agents, http_method,
            is_cover) if is_cover is not None else _filter_and_label_partial(
                api_routes, page_size, agents, http_method)
        return R.success(
            data=[_serialize(api_route,agents) for api_route in api_routes])


def _filter_and_label(api_routes,
                      limit,
                      agents,
                      http_method,
                      is_cover=None,
                      distinct=True,
                      distinct_fields=['path', 'method_id'],
                      distinct_exist_list=[]):
    api_routes_after_filter = []
    distinct_exist_list = distinct_exist_list.copy()
    for api_route in batch_queryset(api_routes):
        distinct_key_ = distinct_key(
            {
                'path': api_route.path,
                'method_id': api_route.method.id
            }, distinct_fields)
        if distinct_key_ in distinct_exist_list:
            continue
        else:
            distinct_exist_list.append(distinct_key_)
        api_route.is_cover = checkcover(api_route, agents, http_method)
        if is_cover is not None:
            api_routes_after_filter += [
                api_route
            ] if api_route.is_cover == is_cover else []
        else:
            api_routes_after_filter += [api_route]
        if limit == len(api_routes_after_filter):
            break
    return api_routes_after_filter


def distinct_key(objects, fields):
    sequence = [objects.get(field, 'None') for field in fields]
    sequence = [
        item if isinstance(item, str) else str(item) for item in sequence
    ]
    return '_'.join(sequence)


def _serialize(api_route, agents):
    item = model_to_dict(api_route)
    is_cover_dict = {1: True, 0: False}
    is_cover_dict = _inverse_dict(is_cover_dict)
    item['is_cover'] = is_cover_dict[api_route.is_cover]
    item['parameters'] = _get_parameters(api_route)
    item['responses'] = _get_responses(api_route)
    item['method'] = _get_api_method(item['method'])
    item['vulnerablities'] = _get_vuls(item['path'], agents)
    return item


def _get_vuls(uri, agents):
    vuls = IastVulnerabilityModel.objects.filter(
        uri=uri, agent_id__in=[_['id'] for _ in agents
                               ]).distinct().values('hook_type_id',
                                                    'level_id').all()
    return [_get_hook_type(vul) for vul in vuls]


def _get_hook_type(vul):

    hook_type = HookType.objects.filter(pk=vul['hook_type_id']).first()
    if hook_type:
        return {'hook_type_name': hook_type.name, 'level_id': vul['level_id']}


def _get_parameters(api_route):
    parameters = IastApiParameter.objects.filter(route=api_route).all()
    parameters = [model_to_dict(parameter) for parameter in parameters]
    parameters = [_get_parameters_type(parameter) for parameter in parameters]
    return parameters


def _get_parameters_type(api_route):
    api_route['parameter_type_shortcut'] = api_route['parameter_type'].split(
        '.')[-1]
    return api_route


def _get_responses(api_route):
    responses = IastApiResponse.objects.filter(route=api_route).all()
    responses = [model_to_dict(response) for response in responses]
    responses = [_get_responses_type(response) for response in responses]
    return responses


def _get_responses_type(api_route):
    api_route['return_type_shortcut'] = api_route['return_type'].split('.')[-1]
    return api_route


def _get_api_method(api_method_id):
    apimethod = IastApiMethod.objects.filter(pk=api_method_id).first()
    if apimethod:
        res = {}
        res['apimethod'] = apimethod.method
        res['httpmethods'] = [_.method for _ in apimethod.http_method.all()]
        return res
    return {}


def _inverse_dict(dic: dict) -> dict:
    return {v: k for k, v in dic.items()}
