from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import MyVueObtainTokenView, MyVueVerifyView, LogoutView, UserViewSet, UserApiView

router = DefaultRouter()

router.register('', UserViewSet, basename='user')

urlpatterns = [
    # path('', UserViewSet.as_view({'get': 'get'}), name='user'),
    # path('', UserApiView.as_view(), name='user'),
    path('login/', MyVueObtainTokenView.as_view(), name='token_obtain_pair'),
    path('info/', MyVueVerifyView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls
