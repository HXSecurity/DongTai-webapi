######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : messages_new
# @created     : 星期三 10月 13, 2021 15:30:46 CST
#
# @description :
######################################################################



from dongtai.utils import const
from dongtai.models.message import IastMessage
from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _



class ResponseDataSerializer(serializers.Serializer):
    new_message_count = serializers.IntegerField(help_text=_('total number of new messages'))
_SuccessSerializer = get_response_serializer(ResponseDataSerializer())


class MessagesNewEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(response_schema=_SuccessSerializer,
                                 summary=_('New Messages Count'),
                                 description=_("Used to get the number of new messages corresponding to the user"),
                                 tags=[_('Messages')])
    def get(self, request):
        return R.success(data={
            'new_message_count':
            IastMessage.objects.filter(to_user_id=request.user.id,
                                       is_read=0).count()
        }, )
