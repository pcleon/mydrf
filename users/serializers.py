# from django.contrib.auth.models import
from rest_framework import serializers
from users.models import MyUser


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('uid', 'username', 'email', 'groups')

class MyUserSerializer(serializers.ModelSerializer):
    role_value = serializers.SerializerMethodField()


    class Meta:
        model = MyUser
        fields = ('username', 'password', 'mobile', 'role_value')

    def create(self, validated_data):
        # user = super().create(validated_date=validated_data)
        user = super(MyUserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_role_value(self, obj):
        return obj.get_role_display()



# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')