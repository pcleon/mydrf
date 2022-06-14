from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User
from users.models import Role, Team


@admin.register(User)
class UserAdm(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'team_name']
    list_display_links = ['username', ]

    fieldsets = (
        ('用户信息', {'fields': ('username', 'password')}),
        (_('用户详情'), {'fields': ('team_name', 'mobile', 'email', 'is_active')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('其他信息'), {'fields': ('last_login', 'date_joined')}),
    )


#
#
class TeamAdm(admin.ModelAdmin):
    list_display = ['team_name']
    list_display_links = ['team_name']
    ordering = ['team_name']


class RoleAdm(admin.ModelAdmin):
    list_display = ['role']

    fieldsets = (
        (_('权限'), {'fields': ('role', 'username')}),
    )
    filter_horizontal = ('username',)


# class RoleUserRelationAdm(admin.ModelAdmin):
#     list_display = ['id', 'username', 'role_id']
#     list_display_links = ['username', 'role_id']
#
#
admin.site.register(Team, TeamAdm)
admin.site.register(Role, RoleAdm)
# admin.site.register(RoleUserRelation, RoleUserRelationAdm)