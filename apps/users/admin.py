from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User
from users.models import Role, Team

admin.site.site_header = 'pcleon的管理页'


@admin.register(User)
class UserAdm(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'team', 'roles']
    list_display_links = ['username', ]
    list_editable = ['email', 'mobile', 'team']
    list_filter = ['team']
    autocomplete_fields = ['team']  # use select2 to select user

    fieldsets = (
        ('用户信息', {'fields': ('username', 'password')}),
        (_('用户详情'), {'fields': ('team', 'mobile', 'email', 'is_active')}),
        # (_('Permissions'), {
        #     'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        # }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('其他信息'), {'fields': ('last_login', 'date_joined')}),
    )


#
#
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
    inlines = [UserInline, ]


class RoleAdm(admin.ModelAdmin):
    list_display = ['role', 'user_list']

    fieldsets = (
        (_('权限'), {'fields': ('role', 'users')}),
    )
    filter_horizontal = ('users',)


# class RoleUserRelationAdm(admin.ModelAdmin):
#     list_display = ['id', 'username', 'role_id']
#     list_display_links = ['username', 'role_id']
#
#
admin.site.register(Team, TeamAdm)
admin.site.register(Role, RoleAdm)
# admin.site.register(RoleUserRelation, RoleUserRelationAdm)