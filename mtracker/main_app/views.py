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
    return redirect('/')

def dashboard(request):
    context = {
        "all_quotes" : Quote.objects.all(),
        "current_user" : User.objects.get(id=request.session['user_id']),
        "all_users" : User.objects.all()
    }
    return render(request, "dashboard.html", context)

