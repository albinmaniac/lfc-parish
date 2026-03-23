from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["created_by", "created_at"]  # ✅ IMPORTANT

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }