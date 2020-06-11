from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = Account
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
