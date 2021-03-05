from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("registerindex", views.regindex),
    path("register", views.register),
    path("login", views.login),
    path("new/ticket", views.newTicket),
    path("create/ticket", views.createTicket),
    path("dashboard", views.dashboard),
    path("ticket/<ticket_id>", views.viewTicket),
    path("ticket/<int:ticket_id>/complete", views.completeTicket),
    path("ticket/<int:ticket_id>/sendmessage", views.sendTicketMessage),
    path("chats", views.chats),
    path("admin", views.admin),
    path("user/<int:user_id>/edit", views.edit),
    path("user/<int:user_id>/update", views.updateUser),
    path("logout", views.logout)
]