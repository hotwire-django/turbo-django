from .models import Message, Room

import turbo
from turbo.shortcuts import render_frame


class RoomListStream(turbo.Stream):
    def add_room(self, room):
        self.append("chat/components/room_list_item.html", {"room": room}, id="room_list")

    def delete_all(self):
        self.remove(selector="#room_list li")


class RoomStream(turbo.ModelStream):
    class Meta:
        model = Room

    def on_save(self, room, created, *args, **kwargs):

        if created:
            # room.turbo.render("chat/components/room_name.html", {"room": room}).append(id="room-list")
            RoomListStream().add_room(room)
        else:
            pass
        # room.turbo.render("chat/room_name.html", {"room": room}).replace(id="update-room")
        # room.turbo.render("chat/room.html", {}).append(id="rooms")

    def user_passes_test(self, user):
        return True


class MessageStream(turbo.ModelStream):
    class Meta:
        model = Message

    def on_save(self, message, created, *args, **kwargs):
        if created:
            message.room.stream.append(
                "chat/components/message.html", {"message": message}, id="messages"
            )
        else:
            message.room.stream.replace(
                "chat/components/message.html", {"message": message}, id=f"message-{message.id}"
            )

    def on_delete(self, message, *args, **kwargs):
        message.room.stream.remove(id=f"message-{message.id}")

    def user_passes_test(self, user):
        return True
