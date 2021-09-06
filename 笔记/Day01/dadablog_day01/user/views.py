import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import UserProfile
import hashlib
#异常码 10100 - 10199


# Create your views here.
#FBV
def user_views(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

#CBV
#更灵活[可继承]
#对未定义的http method请求 直接返回405响应
class UserViews(View):

    # def get(self,request):
    #
    #     return JsonResponse({'code':200,'msg':'test'})

    def post(self, request):

        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']

        #参数基本检查
        #检查用户名是否可用
        #result  = {'code':10100, 'error':'The username is already existed'}
        #return JsonResponse(result)

        #UserProfile插入数据(密码md5存储)
        result = {'code':200, 'username':username, 'data':{}}
        return JsonResponse(result)

