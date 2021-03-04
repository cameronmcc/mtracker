from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("dashboard", views.dashboard),
    path("register", views.register),
    path("login", views.login),
    path("admin", views.admin),
    path("user/<int:user_id>", views.user),
    path("/users/<int:user_id>/update", views.updateUser),
    path("logout", views.logout)
]