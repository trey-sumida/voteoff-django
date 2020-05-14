from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
    class Meta:
        model = Account
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = Account.objects.filter(email=email).count()
        if user_count > 0:
            raise forms.ValidationError("Email has already been registered with another account")
        return email