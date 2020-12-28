from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.apps import apps
from django.template.loader import render_to_string

from turbo import make_channel_name


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.subscriptions = dict()
        self.requests = dict()
        self.accept()

    def notify(self, event, *args, **kwargs):
        model_label = event["model"]
        model = apps.get_model(model_label)

        pk = event["pk"]
        action = event["action"]

        singular_name = model._meta.verbose_name.lower()
        plural_name = model._meta.verbose_name_plural.lower()

        for request_id in self.requests[event["channel_name"]]:
            subscription = self.subscriptions[request_id]
            list_target = subscription.get("list_target") or plural_name
            element_target = f'{subscription.get("element_prefix") or f"{singular_name}_"}{pk}'

            if action == "append" or action == "prepend":
                dom_target = list_target
            else:
                dom_target = element_target

            instance = model.objects.get(pk=pk)
            app, model_name = model_label.lower().split(".")

            self.send_json({
                "request_id": request_id,
                "data": render_to_string('turbo/stream.html', {
                    "object": instance,
                    model_name.lower(): instance,
                    "action": action,
                    "dom_target": dom_target,
                    "model_template": f"{app}/{model_name}.html"
                })
            })

    def receive_json(self, content, **kwargs):
        model_label = content.get("model")
        pk = content.get("pk")
        request_id = content.get("request_id")

        channel_name = make_channel_name(model_label, pk)

        self.subscriptions[request_id] = {
            "list_target": content.get("list_target"),
            "element_prefix": content.get("element_prefix")
        }
        self.requests.setdefault(channel_name, []).append(request_id)
        self.groups.append(channel_name)
        async_to_sync(self.channel_layer.group_add)(channel_name, self.channel_name)
