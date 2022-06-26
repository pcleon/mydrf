from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView,TokenObtainPairView

from users.views import MyVueObtainTokenView, MyVueVerifyView, LogoutView, UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename='user')

urlpatterns = [
    path('login/', MyVueObtainTokenView.as_view(), name='token_obtain'),
    path('info/', MyVueVerifyView.as_view(), name='token_verify'),
    path("logout/", LogoutView.as_view()),
]
urlpatterns += router.urls
print(urlpatterns)