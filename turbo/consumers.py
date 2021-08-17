from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.signing import Signer, BadSignature

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
        if message_type == "subscribe":
            async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
        elif message_type == "unsubscribe":
            async_to_sync(self.channel_layer.group_discard)(
                channel_name, self.channel_name
            )
