# from django.contrib.auth.models import
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source='team.team_name', allow_null=True)
    # team = serializers.CharField(source='team.team_name', allow_blank=True, allow_null=True)
    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'team')
        # extra_kwargs = {'password': {'write_only': True}}


class MyUserSerializer(serializers.ModelSerializer):
    # role_value = serializers.ReadOnlyField(source="get_role_display")
    # roles = Role.objects.get()
    team = serializers.CharField(source='team.team_name', allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'team')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyVueTokenObtainSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["token"] = str(refresh.access_token)
        return data

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')
