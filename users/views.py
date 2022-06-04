from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import VerifyJSONWebToken
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from users.serializers import MyUserSerializer


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


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        authentication_classes = [JSONWebTokenAuthentication]
        permission_classes = [IsAuthenticated]
        d = {"code": 20000,
             "message": "success",
             "data": {}
             }

        return JsonResponse(d)

class MyTokenView(VerifyJSONWebToken):

    # serializer_class = VerifyJSONWebTokenSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params['token'])
        serializer.data = request.query_params['token']

        if serializer.is_valid():
            user = serializer.object.get('users') or request.user
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
            return response

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     允许组查看或编辑的 API 端点。
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
