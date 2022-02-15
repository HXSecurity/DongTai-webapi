#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import R
from iast.base.project_version import version_modify, VersionModifySerializer
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((202, _('Parameter error')), ''),
    ((201, _('Update completed')), ''),
))


class ProjectVersionUpdate(UserEndPoint):
    name = "api-v1-project-version-update"
    description = _("Update application version information")

    @extend_schema_with_envcheck(
        request=VersionModifySerializer,
        tags=[_('Project')],
        summary=_('Projects Version Update'),
        description=_(
            "Update the version information of the corresponding version id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            auth_users = self.get_auth_users(request.user)
            result = version_modify(request.user, auth_users, request.data)
            if not version_id or result.get("status", "202") == "202":
                return R.failure(status=202, msg=_("Parameter error"))
            else:
                return R.success(msg=_('Update completed'))

        except Exception as e:
            logger.error(e)
            return R.failure(status=202, msg=_('Parameter error'))
