from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, ChatRoom, Ticket
import bcrypt

def index(request):
    return render(request, 'index.html')

def regindex(request):
    return render(request, 'register.html')

def register(request):
    errors = User.objects.validate_register(request.POST)

    if errors:
        for value in errors.items():
            messages.error(request, value)
        return redirect("/")
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt() ).decode()
    print(hashed_pw)
    if len(User.objects.all()) < 1 :
        auto_admin = 9
    else:
        auto_admin = 1
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw,
        user_level = auto_admin
    )
    request.session['user_id'] = new_user.id
    print(new_user)
    if new_user.user_level == 9:
        return redirect("/admin")
    return redirect("/dashboard")

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            if logged_user.user_level == 9:
                return redirect("/admin")
            return redirect("/dashboard")
        messages.error(request, "Invalid credentials")
        return redirect('/')
    messages.error(request, "Email doesn't exist, register an account")
    return redirect('/')

def completeTicket(request, ticket_id):
    complete_ticket = Ticket.objects.get(id=ticket_id)
    complete_ticket.completed = True
    complete_ticket.save()
    return redirect("/dashboard")

def admin(request):
    context = {
        "all_tickets" : Ticket.objects.all(),
        "all_users" : User.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "admin.html", context)

def dashboard(request):
    context = {
        "all_tickets" : Ticket.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id']),
        "all_users" : User.objects.all()
    }
    print(context['current_user'].first_name)
    return render(request, "dashboard.html", context)

def chats(request):

    return render(request, "dashboard.html", context)

def admin(request):
    context = {
        "all_tickets" : Ticket.objects.all(),
        "all_users" : User.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "admin.html", context)


def viewTicket(request, ticket_id):
    context = {
        "one_ticket" : Ticket.objects.get(id=ticket_id),
        "current_user" : User.objects.get(id=request.session['user_id']),
        "all_users" : User.objects.all(),
        "all_messages" : Message.objects.all()
    }
    return render(request, "ticket.html", context)

def newTicket(request):
    context = {
        "all_users" : User.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "create_ticket.html", context)

def sendTicketMessage(request, ticket_id):
    print(request.POST)
    errors = Message.objects.validate_message(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"ticket/{ticket_id}")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        new_message = Message.objects.create(
            message = request.POST['message'],
            message_creator = current_user,
            ticket_chat = Ticket.objects.get(id=ticket_id)
        )
        return redirect(f"/ticket/{ticket_id}")

def createTicket(request):
    print(request.POST)
    errors = Ticket.objects.validate_ticket(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/new/ticket")
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        assigned_user = User.objects.get(id=request.POST['assigned_user'])
        new_ticket = Ticket.objects.create(
            task = request.POST['task'],
            description = request.POST['description'],
            completed = False,
            Admin_creator = current_user,
            assigned_user = assigned_user
        )
        
    return redirect("/admin")

def user(request, user_id):
    context = {
        "one_user" : User.objects.get(id=user_id)
    }
    return render(request, "user.html", context)

def edit(request, user_id):
    context = {
        "one_user" : User.objects.get(id=user_id)
    }
    return render(request, "edit.html", context)

def updateUser(request, user_id):
    errors = User.objects.validate_register(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/user/{user_id}/edit")

    update_user = User.objects.get(id = user_id)
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt() ).decode()

    update_user.first_name = request.POST['first_name']
    update_user.last_name = request.POST['last_name']
    update_user.email = request.POST['email']
    update_user.password = hashed_pw
    update_user.save()
    return redirect(f"/user/{user_id}")

    


def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, ticket_id):
    this_ticket = Ticket.objects.get(id= ticket_id)
    this_ticket.delete()
    return redirect("/dashboard")