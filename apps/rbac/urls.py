from django.urls import path
from rest_framework.routers import DefaultRouter
from rbac.views import MyVueObtainTokenView, LogoutView, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('login/', MyVueObtainTokenView.as_view(), name='token'),
    path("logout/", LogoutView.as_view(), name='token'),
    # path("url/", UrlPatternView, name='admin'),
]
urlpatterns += router.urls