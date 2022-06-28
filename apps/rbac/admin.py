from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rbac.models import User, Permission
from rbac.models import Role, Team

admin.site.site_header = 'pcleon的管理页'


class UsershipInline(admin.TabularInline):
    model = User.roles.through


@admin.register(Role)
class RoleAdm(admin.ModelAdmin):
    list_display = ['id', 'role_name', 'permission_list']
    list_display_links = ['role_name', ]
    fieldsets = (
        (_('角色信息'), {'fields': ('role_name', 'permissions')}),
    )

    # inlines = [
    #     UsershipInline,
    # ]
    filter_horizontal = ('permissions',)
    ordering = ('id',)


@admin.register(User)
class UserAdm(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'roles_name']
    list_display_links = ['username', ]
    list_editable = ['email', 'mobile', ]
    # list_filter = ['team_name']
    # autocomplete_fields = ['Team']  # use select2 to select user

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'is_staff', 'email', 'mobile', 'team', 'roles'),
        }),
    )
    fieldsets = (
        ('用户信息', {'fields': ('username', 'password')}),
        (_('用户详情'), {'fields': ('team', 'mobile', 'email', 'is_active')}),
        (_('角色'), {'fields': ('roles',)}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('其他信息'), {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('roles',)


class UserInline(admin.TabularInline):
    model = User
    fields = ['id', 'username', 'email', 'mobile']


class TeamAdm(admin.ModelAdmin):
    list_display = ['id', 'team_name']
    list_display_links = ['id']
    list_editable = ['team_name']
    ordering = ('id',)
    search_fields = ('team_name',)
    # 在详情页里面可以同时编辑userInline信息
    # inlines = [UserInline, ]


admin.site.register(Team, TeamAdm)


class RoleShipInline(admin.TabularInline):
    model = Role.permissions.through
    # fields = ['role_name']

class PermissionAdm(admin.ModelAdmin):
    list_display = ['permission_name', 'uri']
    list_display_links = ['permission_name']
    list_editable = ['uri']

    inlines = [
        RoleShipInline,
    ]


admin.site.register(Permission, PermissionAdm)
