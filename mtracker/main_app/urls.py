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
    path("user/<int:user_id>", views.viewUser),
    path("user/<int:user_id>/edit", views.editUser),
    path("user/<int:user_id>/update", views.updateUser),
    # path("user/<int:user_id>/sendmessage", views.sendUserMessage),
    path("logout", views.logout)
]