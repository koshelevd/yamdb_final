"""Users app URL Configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import UserViewSet, api_user_create, send_token

users_router = DefaultRouter()
users_router.register('users', UserViewSet)

urlpatterns_auth = [
    path('token/obtain/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('email/', api_user_create,
         name='api_user_create'),
    path('token/', send_token,
         name='send_token'),
]

urlpatterns_users = [
    path('auth/', include(urlpatterns_auth)),
    path('', include(users_router.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_users)),
]
