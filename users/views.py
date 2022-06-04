from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import VerifyJSONWebToken, JSONWebTokenAPIView
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from users.serializers import MyUserSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer


class MyUserViewSet(CreateModelMixin, RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer


class MyTokenView(JSONWebTokenAPIView):
    serializer_class = VerifyJSONWebTokenSerializer

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
            res = {"code": 20000,
                   "message": "success",
                   "data": {
                       "name": response_data['data']['name'],
                       "roles": response_data['data']['roles'],
                       "avatar": "https://avatars.githubusercontent.com/u/2787937",
                   }
                   }
            return JsonResponse(res)

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     允许组查看或编辑的 API 端点。
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
