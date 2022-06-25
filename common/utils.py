# 定义装饰器函数
from rest_framework.renderers import JSONRenderer
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

class ApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code*100
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data

        return super().render(response, accepted_media_type, renderer_context)