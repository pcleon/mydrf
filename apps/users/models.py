from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField('手机号', max_length=11, default='', blank=True, null=True)
    # avatar = models.CharField('头像', default='', max_length=100, blank=True, null=True)
    # 通过db_column指定添加的约束的字段名,否则为默认"字段名_id"
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True, null=True, db_column='team',
                             verbose_name='团队')

    def __str__(self):
        return self.username

    def roles(self):
        return [x.get_role_display() for x in self.role_set.all()]

    class Meta:
        db_table = 'my_user'
        # ordering = ['-id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Team(models.Model):
    team_name = models.CharField('团队名', max_length=24, default='', blank=True, unique=True)

    def __str__(self):
        return self.team_name

    class Meta:
        # ordering = ['-id']
        db_table = 'my_team'
        verbose_name = "团队"
        verbose_name_plural = verbose_name


class Role(models.Model):
    role_choices = (
        (0, '管理员'),
        (1, 'DBA'),
        (2, 'admin'),
        (3, 'editor'),
        (4, 'developer'),
    )
    role = models.IntegerField('用户权限', choices=role_choices, blank=True)
    users = models.ManyToManyField('User', db_column='user', db_table='my_user_role', blank=True)

    def user_list(self):
        return [x.get_username() for x in self.users.all()]

    # role_id = models.IntegerField('角色名', choices=role_choices)

    class Meta:
        db_table = 'my_role'
        verbose_name = "用户权限"
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
