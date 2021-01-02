from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.apps import apps
from django.template.loader import render_to_string
from django.core.signing import Signer, BadSignature

from turbo import REMOVE


class TurboStreamException(Exception):
    pass


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.requests = dict()
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

        for request_id in self.requests[event["channel_name"]]:
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

            self.send_json(
                {
                    "request_id": request_id,
                    "data": render_to_string("turbo/stream.html", template_context),
                }
            )

    def receive_json(self, content, **kwargs):
        signer = Signer()
        request_id = content.get("request_id")
        if request_id is None:
            raise TurboStreamException("No request_id in subscription request.")
        message_type = content.get("type")
        if message_type == "subscribe":
            try:
                channel_name = signer.unsign(content.get("signed_channel_name", ""))
            except BadSignature:
                raise TurboStreamException("Signature has been tampered with on the client!")

            self.requests.setdefault(channel_name, []).append(request_id)
            self.groups.append(channel_name)
            async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
        elif message_type == "unsubscribe":
            try:
                channel_name = [channel_name for channel_name, requests in self.requests.items() if request_id in requests][0]
            except IndexError:
                raise TurboStreamException("No subscription for a given request ID exists to unsubscribe.")
            self.groups.remove(channel_name)
            if channel_name not in self.groups:
                async_to_sync(self.channel_layer.group_discard)(channel_name, self.channel_name)
