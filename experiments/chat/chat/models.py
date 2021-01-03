from django.db import models
from django.urls import reverse

from turbo.mixins import BroadcastableModelMixin


class Room(BroadcastableModelMixin, models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Message(BroadcastableModelMixin, models.Model):
    def hi(self):
        self._meta.model_name
    broadcasts_to = ["room", "all-rooms"]
    broadcast_self = False

    def get_turbo_streams_template(self, target):
        if isinstance(target, Room):
            return 'chat/message.html'
        else:
            return 'chat/message_with_room.html'

    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

