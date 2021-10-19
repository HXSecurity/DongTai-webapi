######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : license_upload
# @created     : 星期一 10月 18, 2021 11:59:23 CST
#
# @description :
######################################################################

from base64 import b64decode
from base64 import b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.Random import get_random_bytes
import hashlib
import json
import time

__KEY = b'J6JsALauspvfCUzNUcBm6vfCUzNUcBm6'
IV_LEN = 16
MAC_LEN = 32


def license_validate(license):
    try:
        license_data = decodelicense(license)
        if getmachineid().decode('utf-8') == license_data[
                'deviceId'] and license_data['start_time'] < int(
                    time.time()) < license_data['end_time']:
            return True
        return False
    except:
        return False


def get_license_detail(license):
    try:
        data = decodelicense(license)
        keys = ('max_concurrency', 'start_time', 'end_time', 'target')
        result = {}
        for key in keys:
            result[key] = data[key]
        return result
    except:
        return {}


def getmachineid():
    with open('/sys/class/dmi/id/product_uuid', 'r') as fp:
        MACHINECODE = fp.read()
    return b64encode(
        hashlib.sha256(
            MACHINECODE.strip().encode('utf-8')).hexdigest().encode('utf-8'))


def decodelicense(license):
    return json.loads(
        common_encrypt_decode(common_encrypt_decode(b64decode(license))))


def encodelicense(license):
    licenseId = str(
        hashlib.md5(json.dumps(license).encode('utf-8')).hexdigest()).lower()
    license['licenseId'] = licenseId
    license = json.dumps(license).encode('utf-8')
    return b64encode(common_encrypt_encode(common_encrypt_encode(license)))


def common_encrypt_encode(license):
    raw = license
    iv = get_random_bytes(IV_LEN)
    cipher = AES.new(__KEY, AES.MODE_CBC, iv)
    h = HMAC.new(__KEY, msg=raw, digestmod=SHA256)
    ct = cipher.encrypt(pad(raw, AES.block_size))
    mac = h.digest()
    return iv + mac + ct


def common_encrypt_decode(license):
    raw = license
    iv = raw[:IV_LEN]
    mac = raw[IV_LEN:IV_LEN + MAC_LEN]
    ct = raw[IV_LEN + MAC_LEN:]
    cipher = AES.new(__KEY, AES.MODE_CBC, iv)
    h = HMAC.new(__KEY, digestmod=SHA256)
    msg = unpad(cipher.decrypt(ct), AES.block_size)
    h.update(msg)
    try:
        h.hexverify(mac)
        return msg
    except ValueError:
        return msg


def new_license(machineid, max_concurrency, start_time, end_time, target):
    license = {
        'deviceId': machineid,
        'max_concurrency': max_concurrency,
        'start_time': start_time,
        'end_time': end_time,
        'target': target
    }
    return encodelicense(license)
