from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("dashboard", views.dashboard),
    path("register", views.register),
    path("login", views.login)
]