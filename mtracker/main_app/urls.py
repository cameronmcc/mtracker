from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("dashboard", views.dashboard),
    path("chats", views.chats),
    path("admin", views.admin),
    path("user/<int:user_id>", views.user),
    path("users/<int:user_id>/update", views.updateUser),
    path("logout", views.logout)
]