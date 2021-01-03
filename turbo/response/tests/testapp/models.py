# Django
from django.db import models


class TodoItem(models.Model):
    description = models.TextField()
