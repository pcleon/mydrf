# from django.contrib.auth.models import
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rbac.models import User, Team, Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # query_set或者read_only都可以
    team = serializers.PrimaryKeyRelatedField(source='team.team_name', read_only=True)
    # team = serializers.SlugRelatedField(slug_field='team_name', queryset=Team.objects.all())

    roles = serializers.SlugRelatedField(slug_field='role_name', many=True, queryset=Role.objects.all(),
                                         allow_null=True)

    # roles = RoleSerializer(many=True)
    # permissions = serializers.ManyRelatedField(
    #     serializers.SlugRelatedField(slug_field="username", source="user_id"),
    #     queryset=User.objects.all(),
    #     source="follow"
    # )

    # roles = serializers.ManyRelatedField(
    #     child_relation=serializers.SlugRelatedField(slug_field="role_name", many=True, queryset=Role.objects.all()), source='username')
    # queryset=Role.objects.all(), source="username")

    # def get_roles(self, obj):
    #     return [x.role_name for x in self.roles.all()]
    # roles = RoleSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'mobile', 'email', 'team', 'date_joined',
            'last_login', 'is_active', 'roles', )
        read_only_fields = (
            'id', 'username', 'date_joined', 'last_login'
        )
        extra_kwargs = {
            # 'roles': {'write_only': True},
        }

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def fetch(self, instance, vali):


class MyVueTokenObtainSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["token"] = str(refresh.access_token)
        return data
