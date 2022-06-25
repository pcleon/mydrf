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


class APIResponse(Response):
    def __init__(self, status=20000, msg='ok', http_status=None, headers=None, exception=False, **kwargs):
        # 将外界传入的数据状态码，状态信息以及其他所有额外存储在kwargs中的信息，都格式化成data数据
        data = {
            'status': status,
            'msg': msg
        }
        # 在外界数据可以用result和results来存储
        if kwargs:
            data.update(kwargs)
        super().__init__(data=data, stutus=http_status, headers=headers, exception=exception)
