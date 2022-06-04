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
    mobile = models.CharField('手机号', max_length=11, blank=True, null=True)
    role = models.CharField('角色', choices=role_choices, default='0', max_length=2)
    avatar = models.CharField('头像', default='', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
