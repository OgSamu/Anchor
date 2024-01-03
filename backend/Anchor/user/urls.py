# urls.py
# user.urls.py

from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserLogoutView, UserUpdateView

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="user-register"),
    path("login", UserLoginView.as_view(), name="user-login"),
    path("logout", UserLogoutView.as_view(), name="user-logout"),
    path("<uuid:pk>/goals/", include("goals.urls")),
    path("user/<uuid:pk>/update/", UserUpdateView.as_view(), name="user-update"),
]
