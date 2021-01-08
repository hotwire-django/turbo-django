from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.apps import apps
from django.core.signing import Signer, BadSignature
from django.template.loader import render_to_string

from turbo import REMOVE

signer = Signer()


class TurboStreamException(Exception):
    pass


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def notify_model(self, event):
        model_label = event["model"]
        model = apps.get_model(model_label)
        app, model_name = model_label.lower().split(".")
        instance = model.objects.get(pk=event["pk"])
        event["context"].update(
            {
                "object": instance,
                model_name: instance,
            }
        )

        self.notify(event)

    def notify(
        self,
        event,
    ):
        extra_context = event["context"]
        action = event["action"]
        dom_target = event["dom_target"]

        instance = model.objects.get(pk=pk)
        app, model_name = model_label.lower().split(".")
            template_context = {
                "action": action,
                "dom_target": dom_target,
            }

            # Remove actions don't have contents, so only add context for model
            # template if it's not a remove action.
            if action != REMOVE:
                template_context.update({"model_template": event.get("template")})
                template_context.update({
                    "object": instance,
                    model_name.lower(): instance,
                    "model_template": template,
                    **extra_context,
                }
            )
        signed_channel_name = signer.sign(event["channel_name"])
        self.send_json(
            {
                "signed_channel_name": signed_channel_name,
                "data": render_to_string("turbo/stream.html", template_context),
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
            try:
                channel_name = signer.unsign(content.get("signed_channel_name", ""))
            except BadSignature:
                raise TurboStreamException("Signature has been tampered with on the client!")
            self.requests.setdefault(channel_name, []).append(request_id)
            self.groups.append(channel_name)
            async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
        elif message_type == "unsubscribe":
            async_to_sync(self.channel_layer.group_discard)(
                channel_name, self.channel_name
            )
