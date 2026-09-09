from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm
from .models import CustomUser


def is_admin(user):
    """
    A Django superuser is always treated as an administrator.

    Application users can also be explicitly assigned the `admin` role
    through a trusted administrative process.
    """
    return user.is_superuser or getattr(user, "role", "user") == "admin"


def redirect_authenticated_user(user):
    if is_admin(user):
        return redirect("admin-page")

    return redirect("user-page")


def home(request):
    if request.user.is_authenticated:
        return redirect_authenticated_user(request.user)

    return render(
        request,
        "signup/index.html",
        {
            "login_form": LoginForm(),
            "signup_form": SignupForm(),
        },
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect_authenticated_user(request.user)

    if request.method != "POST":
        return render(
            request,
            "signup/index.html",
            {
                "login_form": LoginForm(),
                "signup_form": SignupForm(),
            },
        )

    form = SignupForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "signup/index.html",
            {
                "login_form": LoginForm(),
                "signup_form": form,
            },
        )

    username = form.cleaned_data["username"]
    email = form.cleaned_data["email"]
    password = form.cleaned_data["password"]

    # Public registration can ONLY create normal users.
    CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        role="user",
    )

    messages.success(
        request,
        "Your account has been successfully created. You can now sign in.",
    )

    return redirect("signin")


def signin(request):
    if request.user.is_authenticated:
        return redirect_authenticated_user(request.user)

    if request.method != "POST":
        return render(
            request,
            "signup/index.html",
            {
                "login_form": LoginForm(),
                "signup_form": SignupForm(),
            },
        )

    form = LoginForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "signup/index.html",
            {
                "login_form": form,
                "signup_form": SignupForm(),
            },
        )

    username = form.cleaned_data["username"]
    password = form.cleaned_data["password"]

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        messages.error(
            request,
            "Incorrect username or password.",
        )

        return render(
            request,
            "signup/index.html",
            {
                "login_form": form,
                "signup_form": SignupForm(),
            },
        )

    login(request, user)

    return redirect_authenticated_user(user)


def logout(request):
    auth_logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("home")
