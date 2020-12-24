from django.db import models
from turbo.mixins import BroadcastableMixin


class Room(models.Model):
    name = models.CharField(max_length=255)


class Message(BroadcastableMixin, models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

