import re

from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User, AnonymousUser

User = get_user_model()


# 验证drf登录
class MyDrfAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

        return (user, None)


# 单method权限
def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)

        return decorated_func

    return decorator


# 自己访问自己
class IsOwner(BasePermission):
    """ 自定义权限只允许对象自身才能获取它。"""

    def has_permission(self, request, view):
        field = view.lookup_field
        return view.kwargs.get(field) == getattr(request.user, field)

    def has_object_permission(self, request, view, obj):
        # 读取权限被允许用于任何请求，
        # 所以我们始终允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in SAFE_METHODS:
            return True
        # 写入权限只允许给 article 的作者:检查文章的作者是不是当前登录的用户
        return obj.user == request.user


# 验证uri是否可以访问,通过uri正则匹配来限制
class MyUriPermissions(BasePermission):

    def __init__(self) -> None:
        pass

    def has_permission(self, request, view):
        # return True
        # 先确认是否为登录用户
        if isinstance(request.user, AnonymousUser):
            return False

        print('使用了permission')
        # return True
        uri = request.path
        # matchPattern = resolve(uri)
        roles = request.user.roles.all()
        # 从角色中获取可以访问的url_name正则列表并去重
        # permissions = roles.permission_reg()
        reg_list = []
        # 逐个从角色中取出正则列表,再逐一对比,匹配成功一个就返回
        for role in roles:
            for reg in role.permission_regex():
                # 忽略重复reg
                if reg in reg_list:
                    continue
                # 匹配直接返回
                elif re.match(reg, uri):
                    return True
                # 添加到列表中
                else:
                    reg_list.append(reg)
        return False
