from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import MyUserViewSet, LogoutView, MyVueObtainTokenView
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

router = SimpleRouter()

router.register('myuser', MyUserViewSet, basename='myuser')

urlpatterns = [
    path('login/', MyVueObtainTokenView.as_view(), name='token_obtain_pair'),
    path('info/', TokenVerifyView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls