# 定义装饰器函数
import json

from django.http import JsonResponse
from rest_framework.response import Response


def MyResponse(func):
    '''
    need dict
    :param func:
    :return:
    '''

    def wrapper(request, *args, **kwargs):
        payload = None
        try:
            payload = func(request, *args, **kwargs)
            assert isinstance(payload, Response) and payload.status_code >= 200, "请求失败"
            data = payload.data
        except Exception as e:
            res = {
                "code": 50000,
                "msg": e.__repr__(),
                "data": payload
            }
            return Response(res)

        res = {
            "code": 20000,
            "msg": "成功",
            "data": payload.data,
        }
        return Response(res)

    return wrapper
