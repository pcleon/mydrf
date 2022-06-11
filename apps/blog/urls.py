from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = DefaultRouter()
router.register('articles', viewset=views.ArticleViewSet, basename='article')
urlpatterns = []
urlpatterns += router.urls

# urlpatterns = [
#     path('articles/', views.ArticleList.as_view()),
#     re_path('articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
# ]
