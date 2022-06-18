# 定义装饰器函数
from rest_framework.response import Response
from functools import wraps



def MyResponse(func):
    '''
    need dict
    :param func:
    :return:
    '''

    # def wrapper(request, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload = None
        try:
            payload = func(*args, **kwargs)
            assert isinstance(payload, Response) and payload.status_code >= 200, "请求失败"
        except Exception as e:
            res = {
                "code": 50000,
                "msg": e.__repr__(),
                "data": payload
            }
            return Response(res)

        payload.data = {
            "code": 20000,
            "msg": "成功",
            "data": payload.data,
        }
        # return Response(res)
        return payload

    return wrapper
