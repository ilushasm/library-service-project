from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import RegisterView, RetrieveUpdateUserView

urlpatterns = [
    path("", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", RetrieveUpdateUserView.as_view(), name="user-profile"),
]

app_name = "user"
