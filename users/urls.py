from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import *

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"),name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path("confirm_logout", confirmar_logout, name="confirmar_logout"),
    path("register/", register, name="register"),
    path("perfil/", perfil_detail, name="perfil_detail"),
    path("perfil/change", perfil_change, name="perfil_edit")
]