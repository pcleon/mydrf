from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Article
from django.contrib.auth import get_user_model

# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=True, allow_blank=True, max_length=90)
#     body = serializers.CharField(required=False, allow_blank=True)
#     author = serializers.ReadOnlyField(source="author.id")
#     status = serializers.ChoiceField(choices=Article.STATUS_CHOICES, default='p')
#     create_date = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         """
#         Create a new "article" instance
#         """
#         return Article.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Use validated data to return an existing `Article`instance。"""
#         instance.title = validated_data.get('title', instance.title)
#         instance.body = validated_data.get('body', instance.body)
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance


class ArticleSerializer(serializers.ModelSerializer):
    # 显示model解析后的数据而非DB中的原始数据
    # 指定author字段的来源(source)为原单个author对象的username，status字段为get_status_display方法返回的完整状态
    # author = serializers.ReadOnlyField(source="author.username")
    #
    author = UserSerializer(read_only=True)
    full_status = serializers.ReadOnlyField(source="get_status_display")
    # full_status = serializers.SerializerMethodField()


    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date', )

    # def get_full_status(self, obj):
    #     return obj.get_status_display()
