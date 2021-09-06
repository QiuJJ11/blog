import json
import time

import jwt
from django.shortcuts import render
from django.http import JsonResponse
from user.models import UserProfile
import hashlib
from django.conf import settings


# 异常码10200-10299
# Create your views here.
def tokens(request):
    if request.method != 'POST':
        result = {'code': 10200, 'error': 'Please use POST!'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']
    # 校验用户名和密码
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        result = {'code': 10201, 'error': 'The username is not existed'}
        return JsonResponse(result)
    p_m = hashlib.md5()
    p_m.update(password.encode())
    if p_m.hexdigest() != user.password:
        result = {'code': 10202, 'error': 'The username or password is wrong'}
        return JsonResponse(result)

    # 记录会话
    token = make_token(username)
    result = {'code': 200, 'username': username, 'data': {'token': token}}
    return JsonResponse(result)


def make_token(username, expire=3600*24):
    key = settings.JWT_TOKEN_KEY
    now_t = time.time()
    payload_data = {'username': username, 'exp': now_t+expire}
    return jwt.encode(payload_data, key, algorithm='HS256')