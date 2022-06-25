from rest_framework import fields, serializers
from .models import BookInfo

# 定义书籍的模型类序列化器


class BookModelSerializer(serializers.ModelSerializer):
    # 可手动加字段
    '''
        ....将字段设置为write_only = True 这样只用与反序列化
            或设置 defult （默认值）
    '''
    num2 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookInfo  # 参考模型类自动生成字段
        # extra_kwargs = {'num2': {'read_only': True}}
        extra_kwargs = {'read_numbers': {'read_only': True}}
        fields = '__all__'

    def get_num2(self, obj):
        return obj.read_numbers*2

    # def to_representation(self, instance):
    # #     """Convert `username` to lowercase."""
    #     ret = super().to_representation(instance)
    # #     # ret['timestamp'] = ret['read_numbers']*2
    #     ret['read_numbers'] = ret['read_numbers']+100
    #     return ret
