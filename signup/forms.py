from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        ),
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "new-password",
            }
        ),
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match.",
            )

        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as exc:
                self.add_error("password", exc)

        return cleaned_data
