from django import forms


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        choices=[('', '--select an option--'), ('admin', 'Admin'), ('user', 'User')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'name': 'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'name': 'password'}), required=True)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'name':'username'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'name': 'email'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'name': 'password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'name': 'confirm_password'}), required=True)
    role = forms.ChoiceField(
        choices=[('', '--select an option--'), ('admin', 'Admin'), ('user', 'User')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
