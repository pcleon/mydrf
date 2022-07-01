import os
import sys
from pathlib import Path
import django
from django.conf import settings
from django.urls import URLPattern, URLResolver

# 添加apps到path查找路径中,方便直接导入
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydrf.settings.dev')
django.setup()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)

for p in list_urls(urlconf.urlpatterns):
    print(''.join(p))