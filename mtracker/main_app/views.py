from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.validate_register(request.POST)

    if errors:
        for value in errors.items():
            messages.error(request, value)
        return redirect("/")
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt() ).decode()
    print(hashed_pw)
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = hashed_pw
    )
    request.session['user_id'] = new_user.id
    return redirect("/dashboard")

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect("/dashboard")
        messages.error(request, "Invalid credentials")
        return redirect('/')
    messages.error(request, "Email doesn't exist, register an account")
    return redirect('/dashboard')

def dashboard(request):
    context = {
        "all_quotes" : Ticket.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id']),
        "all_users" : User.objects.all()
    }
    return render(request, "dashboard.html", context)

def admin(request):
    context = {
        "all_users" : User.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id'])
    }
    return render(request, "admin.html", context)

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
        return redirect(f"/users/{user_id}/edit")

    update_user = User.objects.get(id = user_id)
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt() ).decode()

    update_user.first_name = request.POST['first_name']
    update_user.last_name = request.POST['last_name']
    update_user.email = request.POST['email']
    update_user.password = hashed_pw
    update_user.save()
    return redirect(f"/users/{user_id}")


def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, ticket_id):
    this_ticket = Ticket.objects.get(id= ticket_id)
    this_ticket.delete()
    return redirect("/dashboard")