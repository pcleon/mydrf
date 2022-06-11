# from django.contrib.auth.models import
from rest_framework import serializers
from users.models import MyUser


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('uid', 'username', 'email', 'groups')

class MyUserSerializer(serializers.ModelSerializer):
    role_value = serializers.ReadOnlyField(source="get_role_display")


    class Meta:
        model = MyUser
        fields = ('username', 'mobile', 'role', 'role_value')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = super().create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')