from django.contrib import admin

# Register your models here.
from books.models import BookInfo, HeroInfo


class BookInfoAdm(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'read_numbers', 'comment']
    list_display_links = ['id', 'name']


class HeroInfoAdm(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'comment', 'book']
    list_display_links = ['id', 'name', 'book']


admin.site.register(BookInfo, BookInfoAdm)
admin.site.register(HeroInfo, HeroInfoAdm)
