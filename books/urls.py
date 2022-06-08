from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vue-element-admin/article/list', views.BookModeViewSet, basename='article')

urlpatterns = [
    # path(r'book/<id>', views.BookOneThirdAPIView.as_view()),
    # path(r'book/', views.BookListThirdAPIView.as_view()),
    # path(r'book/', views.BookViewSet.as_view({'get':'list'})),
    # path(r'book/<pk>', views.BookViewSet.as_view({'get':'retrieve'})),
    #  path(r'book/<pk>', views.BookReadOnlyModelViewSet.as_view({'get':'retrieve'})),
    #  path(r'book/', views.BookReadOnlyModelViewSet.as_view({'get':'list'})),
    path(r'book/<pk>', views.BookModeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path(r'book/', views.BookModeViewSet.as_view({'get':'list','post':'create'})),
]

urlpatterns += router.urls