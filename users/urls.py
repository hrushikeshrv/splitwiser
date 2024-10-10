from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users import views

app_name = "users"
urlpatterns = [
    path(
        "login",
        LoginView.as_view(
            template_name="users/login.html",
            redirect_field_name="next",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register", views.UserCreateView.as_view(), name="register"),
]
