import uuid
from django.db import models


class Review(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
