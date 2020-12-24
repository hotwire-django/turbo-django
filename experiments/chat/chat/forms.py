from django.forms import ModelForm
from chat.models import Room, Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["text"]
