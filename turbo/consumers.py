from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.apps import apps
from django.template.loader import render_to_string
from django.core.signing import Signer

from turbo import REMOVE

signer = Signer()


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def notify(self, event, *args, **kwargs):
        template = event["template"]
        extra_context = event["context"]
        model_label = event["model"]
        model = apps.get_model(model_label)

        pk = event["pk"]
        action = event["action"]
        to_list = event["to_list"]

        if to_list:
            dom_target = model._meta.verbose_name_plural.lower()
        else:
            dom_target = f"{model._meta.verbose_name.lower()}_{pk}"

        instance = model.objects.get(pk=pk)
        app, model_name = model_label.lower().split(".")
        template_context = {
            "action": action,
            "dom_target": dom_target,
        }
        # Remove actions don't have contents, so only add context for model
        # template if it's not a remove action.
        if action != REMOVE:
            template_context.update(
                {
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
        channel_name = signer.unsign(content["signed_channel_name"])
        message_type = content["type"]
        if message_type == "subscribe":
            async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
        elif message_type == "unsubscribe":
            async_to_sync(self.channel_layer.group_discard)(
                channel_name, self.channel_name
            )
