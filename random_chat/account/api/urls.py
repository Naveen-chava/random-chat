from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="handler-user-signup"),
    path("login/", views.UserLoginView.as_view(), name="handler-user-login"),
    path("logout/", views.UserLogoutView.as_view(), name="handler-user-logout"),
]
