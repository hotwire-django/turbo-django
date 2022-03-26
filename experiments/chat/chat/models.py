from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)


class Message(models.Model):

    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
