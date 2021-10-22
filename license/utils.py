######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : utils
# @created     : 星期二 10月 19, 2021 17:04:47 CST
#
# @description :
######################################################################

from license.license_encrypt import license_validate, get_license_detail, getmachineid
from dongtai.models.agent import IastAgent
from license.models import IastLicense
import functools
from dongtai.utils import const
import time
from django.core.cache import cache
import re




def is_agent_allowed():

    license_result = license_validate(get_license())
    license_data = get_license_detail(get_license())
    result = license_data and get_agent_concurrency(
    ) <= license_data['max_concurrency'] and license_result
    return result


def get_license():
    license = cache.get('license', None)
    if license is None:
        license_obj = IastLicense.objects.filter(key='license').first()
        if license_obj is None:
            license = ''
        else:
            license = license_obj.value
    if license:
        cache.set('license', license, 60 * 2)
    return license


def get_agent_concurrency():
    res = IastAgent.objects.filter(online=const.RUNNING).count()
    return res


def delete_license():
    cache.set('license', None, 60 * 2)
    IastLicense.objects.filter(key='license').delete()
    cache.set('license', None, 60 * 2)


def store_license(license):

    obj, created = IastLicense.objects.update_or_create(
        {
            'key': 'license',
            'value': license
        }, key='license')
    cache.set('license', license, 60 * 2)
    return created


def url_validate(url):
    whitelist = [
        '/api/v1/license/.*', '/api/v1/user/info', '/api/v1/user/login',
        '/api/v1/user/logout', '/api/v1/captcha/.*', '/api/v1/i18n/setlang',
        '/api/v1/message/.*', '/upload/.*'
    ]
    for pattern in whitelist:
        if re.match(pattern, url):
            return True
    return False
