from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class MyUser(AbstractUser):
    role_choices = (
        ('0', '管理员'),
        ('1', 'DBA'),
        ('2', 'admin'),
        ('3', 'editor'),
        ('4', 'developer'),
    )
    mobile = models.CharField('手机号', max_length=11, default='', blank=True, null=True)
    role = models.CharField('角色', choices=role_choices, default='0', max_length=2)
    avatar = models.CharField('头像', default='', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "用户"
        verbose_name_plural = verbose_name

# django.contrib.auth.backends获取auth模块的验证和⽤户的信息
# class CustomBackend(ModelBackend):
#     def authenticate(self, username=None, password=None, **kwargs):
#         try:
#             user = MyUser.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None
