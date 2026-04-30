from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate 
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Accounts

# Create your views here.

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request, user)
            return render(request, "dashboard.html")
        
        messages.error(request, "Your username or password is incorrect")
        return redirect('signin')
        
    return render(request, 'sign-in.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get('email')
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exits")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email ID alredy exits, please try with the different email ID")
            return redirect("signup")
        
        if password != confirm_password:
            messages.error(request, "The password does not match")
            return redirect("signup")

        if len(password) < 8:
            messages.error(request, "You atleast need 8 chracters to create a password")
            return redirect("signup")
        
        create_user = User.objects.create(
            username=username,
            email=email,
            password=password,
        )

        create_user.save()
        return redirect('signin')
    
    return render(request, 'signup.html')