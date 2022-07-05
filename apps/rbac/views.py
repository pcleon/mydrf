from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from common.pagination import MyPageNumberPagination
from common.permissions import MyUriPermissions, IsOwner, method_permission_classes
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

        return Response(serializer.validated_data, status=HTTP_200_OK)


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

        return Response({"token": serializer.validated_data.get('access')}, status=HTTP_200_OK)


class UserViewSet(ReadOnlyModelViewSet):
    """
    允许用户查看或编辑的 API 端点。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']

    permission_classes = (MyUriPermissions,)

    @method_permission_classes([IsOwner])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @action(methods=['GET', 'POST'], detail=False, permission_classes=[IsAuthenticated])
    def info(self, request):
        '''
        token
        用户信息
        '''

        # 使用IsAuthenticated就不需要try了,使用AllowAny需要
        try:
            uid = request.META.get('USER')
        except AttributeError:
            raise ValidationError(detail='verify fail', code=HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=uid)
        u_info = {
            "uid": user.id,
            "name": user.username,
            "team": user.team.team_name,
            "roles": user.roles_name(),
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


# 只做登录用户和密码的认证
class MyAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
