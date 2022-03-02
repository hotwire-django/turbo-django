from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.signing import Signer, BadSignature

import logging

from .registry import channel_for_channel_name
from .utils import to_subscribable_name

logger = logging.getLogger("turbo.streams")

signer = Signer()


class TurboStreamException(Exception):
    pass


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def notify(self, event):
        signed_channel_name = signer.sign(event["channel_name"])
        self.send_json(
            {
                "signed_channel_name": signed_channel_name,
                "data": event.get("rendered_template"),
            }
        )

    def receive_json(self, content, **kwargs):

        try:
            channel_name = signer.unsign(content["signed_channel_name"])
        except (BadSignature, KeyError):
            raise TurboStreamException(
                "Signature is invalid or not present. This could be due to a misbehaving client."
            )

        message_type = content["type"]

        Channel, is_model_channel, pk = channel_for_channel_name(channel_name)
        if is_model_channel:
            channel = Channel.from_pk(pk)
        elif Channel:
            channel = Channel()
        else:
            logger.warning("Channel '%s' could not be located.", channel_name)
            return

        self.subscribe_to_channel(message_type, channel, self.scope.get("user"))

    def subscribe_to_channel(self, message_type, channel, user):

        if not channel.user_passes_test(user):
            logger.warning(
                "User `%s` does not have permission to access channel '%s'.",
                user,
                channel.channel_name,
            )
            return False

        channel_name = to_subscribable_name(channel.channel_name)

        if message_type == "subscribe":
            async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
        elif message_type == "unsubscribe":
            async_to_sync(self.channel_layer.group_discard)(channel_name, self.channel_name)
