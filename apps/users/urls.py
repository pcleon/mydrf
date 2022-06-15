from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import MyVueObtainTokenView, MyVueVerifyView, LogoutView, MyUserViewSet, UserApiView

router = SimpleRouter()

router.register('myuser', MyUserViewSet, basename='myuser')

urlpatterns = [
    path('', UserApiView.as_view(), name='user'),
    path('login/', MyVueObtainTokenView.as_view(), name='token_obtain_pair'),
    path('info/', MyVueVerifyView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls
