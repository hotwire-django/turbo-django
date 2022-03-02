from chat.models import Room
from django import forms


class RoomForm(forms.ModelForm):

    name = forms.CharField(label="Room Name", required=False)

    class Meta:
        model = Room
        fields = ('name',)
