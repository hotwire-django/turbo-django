from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model

default_app_config = 'turbo.apps.TurboDjangoConfig'


def make_channel_name(model_label, pk):
    return f"BROADCAST-{model_label}-{pk}".lower()


def get_channel_name(identifier):
    if isinstance(identifier, Model):
        return _channel_name_for_instance(identifier)
    else:
        return identifier.__str__()


def _channel_name_for_instance(instance: Model):
    return make_channel_name(instance._meta.label, instance.pk)


# Model actions
CREATED = "CREATED"
UPDATED = "UPDATED"
DELETED = "DELETED"

# Turbo Streams CRUD operations
APPEND = "append"
PREPEND = "prepend"
REPLACE = "replace"
REMOVE = "remove"


def send_broadcast(stream_target, dom_target, action, template, context):
    """
    Send a Broadcast to all Websocket Clients registered to a specifc stream!
    """
    channel_layer = get_channel_layer()
    channel_name = get_channel_name(stream_target)
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            "type": "notify",
            "action": action,
            "channel_name": channel_name,
            "template": template,
            "context": context,
            "dom_target": dom_target,
        },
    )
