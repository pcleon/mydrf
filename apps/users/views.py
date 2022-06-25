from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User
from users.serializers import UserSerializer
from common.utils import MyResponse

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserTokenVerifyView(TokenVerifyView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])


        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyVueObtainTokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    # 自己定义,只返回想要的access,使用TokenObtainPairSerializer会返回refresh和access
    # serializer_class = MyVueTokenObtainSerializer

    # 只返回token字段
    @MyResponse
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({"token": serializer.validated_data.get('access')}, status=status.HTTP_200_OK)


class MyVueVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @MyResponse
    def get(self, request):
        token = request.query_params.get("token")
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
        u_info = {
            "uid": user.id,
            "name": user.username,
            "team": user.team.team_name,
            "roles": [x.get_role_display() for x in user.roles.all()],
            "email": user.email,
            "avatar": "https://avatars.githubusercontent.com/u/2787937?s=100",
            "introduction": f"我是{user.username}, 哈哈哈哈!!"
        }

        return Response(u_info)


# class UserApiView(APIView):
#     @MyResponse
#     def get(self, request):
#         obj = User.objects.all()
#         serializer = UserSerializer(obj, many=True)
#         d = {
#             'total': len(serializer.data),
#             'items': serializer.data
#         }
#
#         return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # 按用户名查找
    lookup_field = 'username'

    @MyResponse
    # def get(self, request):
    def list(self, request):
        query_set = self.get_queryset()
        serializer = UserSerializer(query_set, many=True)
        res = {
            'total': len(serializer.data),
            'items': serializer.data
        }

        return Response(res)


class LogoutView(APIView):
    """
    登出
    """

    @MyResponse
    def post(self, request):
        data = "logout"
        return Response(data)

class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None