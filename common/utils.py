# 定义装饰器函数
import json

from django.http import JsonResponse

def MyResponse(func):
    def wrapper(request, *args, **kwargs):
        data_dic = None
        try:
            data_dic = func(request, *args, **kwargs)
            assert isinstance(data_dic, JsonResponse) and data_dic.status_code >= 200
        except Exception as e:
            res = dict(code=50000, msg=f'{e.__repr__()}', data=f'{data_dic}')
            return JsonResponse(res)

        res = dict(code=20000, msg='成功', data=json.loads(data_dic.content))
        return JsonResponse(res)
    return wrapper
