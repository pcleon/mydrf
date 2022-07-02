from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField('手机号', max_length=11, default='', blank=True, null=True)
    # avatar = models.CharField('头像', default='', max_length=100, blank=True, null=True)
    # 通过db_column指定添加的约束的字段名,否则为默认"字段名_id"
    team = models.ForeignKey('Team', on_delete=models.CASCADE, db_column='team', verbose_name='小组')

    roles = models.ManyToManyField('Role', db_column='roles', db_table='rbac_user_role', blank=True, verbose_name='角色')

    def __str__(self):
        return self.username

    def roles_name(self):
        return [x.role_name for x in self.roles.all()]

    class Meta:
        db_table = 'rbac_user'
        ordering = ['id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Team(models.Model):
    team_name = models.CharField('小组名', max_length=24, default='', unique=True)

    def __str__(self):
        return self.team_name

    class Meta:
        # ordering = ['-id']
        db_table = 'rbac_team'
        verbose_name = "小组"
        verbose_name_plural = verbose_name


class Role(models.Model):
    role_name = models.CharField('角色', max_length=20, unique=True)
    permissions = models.ManyToManyField('Permission', db_column='permissions', db_table='rbac_role_permission', blank=True, verbose_name='权限',)

    def permission_regex(self):
        # permissions = self.permissions.all()
        # return [x.uri for x in self.permissions.all()]
        p_list = []
        for permission in self.permissions.all():
            p_list += permission.uri.strip().split(',')
        return list(dict.fromkeys(p_list))

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'rbac_role'
        verbose_name = "角色"
        verbose_name_plural = verbose_name

class Permission(models.Model):
    permission_name = models.CharField('权限名', max_length=50, unique=True)
    uri = models.CharField('uri正则(,分隔)', max_length=200, default='', unique=True)

    def __str__(self):
        return self.permission_name

    class Meta:
        db_table = 'rbac_permission'
        verbose_name = "api权限"
        verbose_name_plural = verbose_name


#
# class RoleUserRelation(models.Model):
#     user_id = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
#     role_id = models.ForeignKey('Role', on_delete=models.CASCADE, db_column='role_id')
#
#     def __str__(self):
#         return self.user_id
#
#     class Meta:
#         db_table = 'my_user_role'
#         verbose_name = "用户角色关系"
#         verbose_name_plural = verbose_name

# django.contrib.auth.backends获取auth模块的验证和⽤户的信息
# class CustomBackend(ModelBackend):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#             user = MyUser.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None
