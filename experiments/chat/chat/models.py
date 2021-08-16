from django.db import models

from turbo.mixins import TurboMixin


class Room(TurboMixin, models.Model):
    name = models.CharField(max_length=255)


class Message(TurboMixin, models.Model):

    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
