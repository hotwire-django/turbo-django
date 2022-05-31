import turbo
from quickstart.models import Review


class BroadcastStream(turbo.Stream):
    pass


class RatingStream(turbo.ModelStream):
    class Meta:
        model = Review
