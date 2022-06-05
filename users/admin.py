from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import MyUser


@admin.register(MyUser)
class MyUserAdm(UserAdmin):
    list_display = ['username', 'role', 'mobile']
    list_display_links = ['username']

    fieldsets = (
        ('用户信息', {'fields': ('username', 'password')}),
        (_('用户详情'), {'fields': ('mobile', 'email', 'role', 'is_active')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('其他信息'), {'fields': ('last_login', 'date_joined')}),
    )