from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from common.pagination import MyPageNumberPagination
from common.permissions import MyUrlNamePermissions
from rbac.serializers import UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

User = get_user_model()


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
    # @MyResponse
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response({"token": serializer.validated_data.get('access')}, status=status.HTTP_200_OK)


class MyVueVerifyView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # @MyResponse
    def get(self, request):
        # def user_info(self, request):
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

    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticatedOrReadOnly])
    # @action(methods=['GET'], detail=False, name='userinfo', permission_classes=[IsAuthenticatedOrReadOnly, MyUrlNamePermissions])
    def info(self, request):
        '''
        token
        用户信息
        '''
        token = request.query_params.get("token")
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
        u_info = {
            "uid": user.id,
            "name": user.username,
            "team": user.team.team_name,
            "roles": [x.role_name for x in user.roles.all()],
            "email": user.email,
            "avatar": "https://avatars.githubusercontent.com/u/2787937?s=100",
            "introduction": f"我是{user.username}, 哈哈哈哈!!"
        }

        return Response(u_info)

    # 分页
    pagination_class = MyPageNumberPagination
    # 按用户名查找
    lookup_field = 'username'


class LogoutView(APIView):
    """
    登出
    """
    permission_classes = (AllowAny,)

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
