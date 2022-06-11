from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import SimpleRouter

from users.views import MyUserViewSet, MyTokenView, LogoutView

router = SimpleRouter()

router.register('myuser', MyUserViewSet, basename='myuser')

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("info/", MyTokenView.as_view()),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls