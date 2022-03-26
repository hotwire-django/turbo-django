from django import forms
from reminders.models import Reminder


class ReminderForm(forms.ModelForm):

    reminder_text = forms.CharField(label="Add", required=False)

    class Meta:
        model = Reminder
        fields = ('reminder_text',)
