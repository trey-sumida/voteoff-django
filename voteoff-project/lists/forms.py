from django import forms
from django.forms import ModelForm
from .models import Contest, Choice


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ["contest_title", "contest_description", "public", "start_date", "end_date"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].widget = DateTimeInput()
        self.fields["start_date"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields["end_date"].widget = DateTimeInput()
        self.fields["end_date"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]