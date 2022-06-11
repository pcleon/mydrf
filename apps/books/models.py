from django.db import models
from django.db.models.base import Model


# 定义BookInfo
class BookInfo(models.Model):
    name = models.CharField(max_length=20, verbose_name='图书名称')
    create_time = models.DateField(verbose_name='发布日期')
    read_numbers = models.IntegerField(default=0, verbose_name='阅读量')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='评论')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'books_book'  # 指明数据库表名
        verbose_name = '图书'  # admin显示名称
        verbose_name_plural = verbose_name

    def __str__(self):
        '''定义每个数据对象的显示信息'''
        return self.name


class HeroInfo(models.Model):
    gender_choices = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(choices=gender_choices, blank=False, default=0, verbose_name='性别')
    name = models.CharField(max_length=20, verbose_name='名称')
    comment = models.CharField(max_length=255, blank=True)
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)

    def __str__(self):
        '''定义每个数据对象的显示信息'''
        return self.name

    class Meta:
        db_table = 'books_heroinfo'  # 指明数据库表名
        verbose_name = '人物角色'  # admin显示名称
        verbose_name_plural = verbose_name
