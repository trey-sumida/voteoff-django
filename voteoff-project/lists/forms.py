from django import forms
from django.forms import ModelForm
from .models import Contest, Choice


class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ["contest_title", "contest_description", "public"]
