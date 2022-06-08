from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from users.models import MyUser
from users.serializers import MyUserSerializer
from common.utils import MyResponse

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
# jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class LogoutView(APIView):
    """
    登出
    """
    def post(self, req):
        return JsonResponse({
            'code': 20000,
            'data': 'success'
        })


class MyUserViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer


class MyTokenView(JSONWebTokenAPIView):
    serializer_class = VerifyJSONWebTokenSerializer

    @MyResponse
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params.dict())

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)

            obj = MyUser.objects.get(username=user.username)
            user_info = MyUserSerializer(obj).data
            res = {
                "name": user_info['username'],
                "roles": [user_info['role_value']],
                "introduction": f"I am a {user_info['role_value']}",
                "avatar": "https://avatars.githubusercontent.com/u/2787937",
            }
            return JsonResponse(res)
