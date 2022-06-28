from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rbac.views import MyVueObtainTokenView, LogoutView, UserViewSet


router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('login/', MyVueObtainTokenView.as_view(), name='token_obtain'),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls