from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User
from users.models import Role, Team

admin.site.site_header = 'pcleon的管理页'


class UsershipInline(admin.TabularInline):
    model = User.roles.through


@admin.register(Role)
class RoleAdm(admin.ModelAdmin):
    list_display = ['role']
    fieldsets = (
        (_('角色'), {'fields': ('role',)}),
    )

    inlines = [
        UsershipInline,
    ]


@admin.register(User)
class UserAdm(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'team', 'roles_name']
    list_display_links = ['username', ]
    list_editable = ['email', 'mobile', 'team']
    list_filter = ['team']
    autocomplete_fields = ['team']  # use select2 to select user

    fieldsets = (
        ('用户信息', {'fields': ('username', 'password')}),
        (_('用户详情'), {'fields': ('team', 'mobile', 'email', 'is_active')}),
        (_('角色'), {'fields': ('roles', 'user_permissions')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('其他信息'), {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('roles',)


#
#
class UserInline(admin.TabularInline):
    model = User
    fields = ['id', 'username', 'email', 'mobile']


@admin.register(Team)
class TeamAdm(admin.ModelAdmin):
    list_display = ['id', 'team_name']
    list_display_links = ['id']
    list_editable = ['team_name']
    ordering = ('id',)
    search_fields = ('team_name',)
    # 在详情页里面可以同时编辑userInline信息
    inlines = [UserInline, ]

# class RoleUserRelationAdm(admin.ModelAdmin):
#     list_display = ['id', 'username', 'role_id']
#     list_display_links = ['username', 'role_id']
#
#
# admin.site.register(RoleUserRelation, RoleUserRelationAdm)
