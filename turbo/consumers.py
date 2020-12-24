from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.apps import apps
from django.template.loader import render_to_string

from turbo import get_broadcast_channel


class TurboStreamsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.subscriptions = dict()
        self.requests = dict()
        self.accept()

    def notify(self, event, *args, **kwargs):
        model_label = event["model"]
        model = apps.get_model(model_label)

        pk = event["pk"]
        stream = event["stream"]
        model_action = event["action"]


        singular_name = model._meta.verbose_name.lower()
        plural_name = model._meta.verbose_name_plural.lower()

        for request_id in self.requests[event["channel"]]:
            subscription = self.subscriptions[request_id]
            list_target = subscription.get("list_target") or plural_name
            element_target = f'{subscription.get("element_prefix") or f"{singular_name}_"}{pk}'

            if stream == "pk":
                target = element_target
                stream_action = "replace"
            elif model_action == "CREATE":
                target = list_target
                stream_action = "append"
            elif model_action == "UPDATE":
                target = element_target
                stream_action = "replace"
            elif model_action == "DELETE":
                target = element_target
                stream_action = "remove"
            else:
                return

            instance = model.objects.get(pk=pk)
            app, model_name = model_label.lower().split(".")

            self.send_json({
                "request_id": request_id,
                "data": render_to_string('turbo/stream.html', {
                    "object": instance,
                    model_name.lower(): instance,
                    "action": stream_action,
                    "dom_target": target,
                    "model_template": f"{app}/{model_name}.html"
                })
            })

    def receive_json(self, content, **kwargs):
        model_label = content.get("model")
        stream = content.get("stream")
        value = content.get("value")
        request_id = content.get("request_id")

        channel = get_broadcast_channel(model_label.lower(), stream, value)

        self.subscriptions[request_id] = {
            "list_target": content.get("list_target"),
            "element_prefix": content.get("element_prefix")
        }
        self.requests.setdefault(channel, []).append(request_id)
        print(f"RECEIVED SUBSCRIPTION: {channel}")
        self.groups.append(channel)
        async_to_sync(self.channel_layer.group_add)(channel, self.channel_name)
