from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.signing import Signer, BadSignature

import logging

from .registry import stream_for_stream_name

logger = logging.getLogger("turbo.streams")

signer = Signer()


class TurboStreamException(Exception):
    pass


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def notify(self, event):
        self.send_json(
            {
                "signed_channel_name": event["signed_channel_name"],
                "data": event.get("rendered_template"),
            }
        )

    def receive_json(self, content, **kwargs):
        try:
            stream_name, args, kwargs = signer.unsign_object(content["signed_channel_name"])
        except (BadSignature, KeyError):
            raise TurboStreamException(
                "Signature is invalid or not present. This could be due to a misbehaving client."
            )

        message_type = content["type"]
        Stream = stream_for_stream_name(stream_name)

        if Stream:
            stream = Stream(*args, **kwargs)
        else:
            logger.warning("Stream '%s' could not be located.", stream_name)
            return

        self.subscribe_to_stream(message_type, stream, self.scope.get("user"))

    def subscribe_to_stream(self, message_type, stream, user):
        if not stream.user_passes_test(user):
            logger.warning(
                "User `%s` does not have permission to access stream '%s'.",
                user,
                stream.stream_name,
            )
            return False

        stream_name = stream.broadcastable_stream_name
        if message_type == "subscribe":
            async_to_sync(self.channel_layer.group_add)(stream_name, self.channel_name)
        elif message_type == "unsubscribe":
            async_to_sync(self.channel_layer.group_discard)(stream_name, self.channel_name)
