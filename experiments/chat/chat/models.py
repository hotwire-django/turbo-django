from django.db import models
from django.urls import reverse

from turbo.mixins import BroadcastableMixin


class Room(BroadcastableMixin, models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class Message(BroadcastableMixin, models.Model):
    broadcasts_to = ["room", "all-rooms"]
    broadcast_self = False

    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
