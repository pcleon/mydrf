from django.http import JsonResponse
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework.routers import SimpleRouter

from users.views import MyUserViewSet

router = SimpleRouter()

router.register('myuser', MyUserViewSet, basename='myusers')

urlpatterns = [
    path("login/", obtain_jwt_token),
    # path("info/", MyTokenView.as_view()),
    path("info/", verify_jwt_token),
    # path("info1/", verify_jwt_token),
]
urlpatterns += router.urls