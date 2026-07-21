from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import CustomUser


def home(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'signup/index.html', {'login_form': login_form, 'signup_form': signup_form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, 'signup/index.html', {'signup_form': form, 'login_form': LoginForm()})
            
            existing_user = CustomUser.objects.filter(email=email).first()
            
            if existing_user is not None:
                if existing_user.username == username:
                    messages.info(request, 'Username already exists')
                elif existing_user.role == role:
                    messages.error(request, 'User with the same email and role already exists')
                else:
                    myuser = CustomUser.objects.create_user(username, email, password)
                    myuser.role = role
                    myuser.save()
                    messages.success(request, 'Your account has been successfully created.')
                    return redirect('signin')
            else:
                myuser = CustomUser.objects.create_user(username, email, password)
                myuser.role = role
                myuser.save()
                messages.success(request, 'Your account has been successfully created.')
                return redirect('signin')
        else: 
            return render(request, 'signup/index.html', {'signup_form': form, 'login_form': LoginForm()})
    else:
        form = SignupForm()
    
    return render(request, 'signup/index.html', {'signup_form': form, 'login_form': LoginForm()})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                is_super = getattr(user, 'is_superuser', False)
                user_role = getattr(user, 'role', 'admin' if is_super else 'user')

                if user_role == 'admin':
                    return redirect('admin-page')
                elif user_role == 'user':
                    return redirect('user-page')
            else:
                messages.error(request, "Incorrect username or password")
        return render(request, 'signup/index.html', {'login_form': form, 'signup_form': SignupForm()})

    return render(request, 'signup/index.html', {'login_form': LoginForm(), 'signup_form': SignupForm()})


def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

