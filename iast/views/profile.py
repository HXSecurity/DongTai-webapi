from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from webapi.settings import config
from dongtai.models.profile import IastProfile
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.forms.models import model_to_dict

class ProfilepostArgsSer(serializers.Serializer):
    value = serializers.CharField(help_text=_('profile value'))

class ProfileEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(summary=_('Get Profile'),
                                 description=_("Get Profile with key"),
                                 tags=[_('Profile')])
    def get(self, request, key):
        profile = IastProfile.objects.filter(key=key).values_list(
            'value', flat=True).first()
        if profile is None:
            return R.failure(
                msg=_("Failed to get {} configuration").format(key))
        return R.success(data={key: profile})

    @extend_schema_with_envcheck(summary=_('Profile modify'),
                                request=ProfilepostArgsSer,
                                 description=_("Modifiy Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request, key):
        if not request.user.is_talent_admin():
            return R.failure(
                msg=_("Current users have no permission to modify"))
        ser = ProfilepostArgsSer(data=request.data)
        try:
            if ser.is_valid(True):
                value = ser.validated_data['value']
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            obj, created = IastProfile.objects.update_or_create(key=key,
                                                                value=value)
        except Exception as e:
            print(e)
            return R.failure(msg=_("Update {} failed").format(key))
        return R.success(data={key: obj.value})

class ProfileBatchGetArgsSer(serializers.Serializer):
    keys = serializers.ListField(help_text=_('profile key'))

class ProfileBatchGetEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(summary=_('GetProfileBatch'),
                                 request=ProfileBatchGetArgsSer,
                                 description=_("Get Profile with key batch"),
                                 tags=[_('Profile')])
    def post(self, request):
        keys = request.data.get('keys', None)
        profiles = IastProfile.objects.filter(key__in=keys).all()
        if profiles is None:
            return R.failure(
                msg=_("Failed to get configuration"))
        return R.success(data=[model_to_dict(profile) for profile in profiles])


class ProfileBatchPostArgsSer(serializers.Serializer):
    value = serializers.CharField(help_text=_('profile value'))
    key = serializers.CharField(help_text=_('profile key'))


class ProfileBatchModifiedEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(summary=_('Profile modify'),
                                 request=ProfileBatchPostArgsSer(many=True),
                                 description=_("Modifiy Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request):
        if not request.user.is_talent_admin():
            return R.failure(
                msg=_("Current users have no permission to modify"))
        ser = ProfileBatchPostArgsSer(data=request.data, many=True)
        try:
            if ser.is_valid(True):
                data = ser.validated_data
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            for i in data:
                obj, created = IastProfile.objects.update_or_create(
                    **i)
        except Exception as e:
            print(e)
            return R.failure(msg=_("Update configuration failed"))
        return R.success(data=data)


def get_model_field(model, exclude=[], include=[]):
    fields = [field.name for field in model._meta.fields]
    if include:
        return [
            include for field in list(set(fields) - set(exclude))
            if field in include
        ]
    return list(set(fields) - set(exclude))
