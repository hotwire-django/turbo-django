import turbo


class TurboMixin:

    """
    Mixin that attaches a .turbo attribute to a django model.
    This allows for any instance to broadcast to pages listening to the
    object channel.

    Instances must have a primary key assigned to be broadcast, or else a ValueError
    will be thown.

    Ex:
        room = Room.objects.first()
        room.turbo.render("chat/room_name.html", {"room": room}).replace(id="update-room")
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turbo = turbo.classes.Turbo(self)
