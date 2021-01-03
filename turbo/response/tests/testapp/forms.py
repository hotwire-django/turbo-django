# Django
from django import forms

# Local
from .models import TodoItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ("description",)
