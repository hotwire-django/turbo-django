
from .models import Message, Room

import turbo
from turbo.shortcuts import render_frame

class RoomListChannel(turbo.Channel):

    def add_room(self, room):
        print(vars(room))
        self.append(
            "chat/components/room_list_item.html",
            {
                "room": room
            },
            id="room_list"
        )

    def delete_all(self):
        self.remove(selector="#room_list li")


class RoomChannel(turbo.ModelChannel):

    class Meta:
        model = Room

    def on_save(self, room, created, *args, **kwargs):

        if created:
            #room.turbo.render("chat/components/room_name.html", {"room": room}).append(id="room-list")
            RoomListChannel().add_room(room)
        else:
            pass
        # room.turbo.render("chat/room_name.html", {"room": room}).replace(id="update-room")
        # room.turbo.render("chat/room.html", {}).append(id="rooms")


    def user_passes_test(self, user):
        return True


class MessageChannel(turbo.ModelChannel):

    class Meta:
        model = Message

    def on_save(self, message, created, *args, **kwargs):
        if created:
            message.room.channel.append("chat/components/message.html", {"message": message}, id="messages")
        else:
            message.room.channel.replace("chat/components/message.html", {"message": message}, id=f"message-{message.id}")

    def on_delete(self, message, *args, **kwargs):
        message.room.channel.remove(id=f"message-{message.id}")

    def user_passes_test(self, user, object_id):
        return True

