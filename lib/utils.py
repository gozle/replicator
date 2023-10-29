import hmac
import base64
import hashlib


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_hmac(key, value):
    hmac_hash = hmac.new(base64.b64encode(key.encode('utf-8')), value.encode('utf-8'), hashlib.sha256)
    return hmac_hash
