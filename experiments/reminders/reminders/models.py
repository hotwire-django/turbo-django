from django.db import models
from django.urls import reverse


class Reminder(models.Model):

    reminder_text = models.CharField(max_length=255)
    completed_date = models.DateTimeField(null=True, blank=True)
    order = models.IntegerField(default=0)
