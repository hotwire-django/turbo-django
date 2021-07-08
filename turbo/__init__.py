from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model

default_app_config = "turbo.apps.TurboDjangoConfig"


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
UPDATE = "update"
REMOVE = "remove"
BEFORE = "before"
AFTER = "after"


def broadcast_stream(
    stream_target,
    action,
    template,
    context,
    dom_target=None,
    css_selector=None,
    send_type="notify",
    extra_payload=None,
):
    """
    Send a Broadcast to all Websocket Clients registered to a specific stream!
    """
    if extra_payload is None:
        extra_payload = dict()

    if dom_target is None != css_selector is None:
        raise ValueError('Either dom_target or css_selector must be set as a parameter to broadcast_stream().')

    channel_layer = get_channel_layer()
    channel_name = get_channel_name(stream_target)
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            "type": send_type,
            "action": action,
            "channel_name": channel_name,
            "template": template,
            "context": context,
            "dom_target": dom_target,
            "css_selector": css_selector,
            **extra_payload,
        },
    )


from collections import namedtuple
BroadcastTarget = namedtuple('BroadcastTarget', ['selector_type', 'selector', 'action'])

class Broadcast():

    def __init__(self, stream_name=None, send_type='notify'):
        self.stream_name = stream_name
        self.send_type = send_type
        self._targets = []

    def _chain(self):
        """
        Return a copy of the current Broadcast that's ready for another operation.
        """
        c = self.__class__(stream_name=self.stream_name)
        c._targets = self._targets
        return c

    def append(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, APPEND)

    def prepend(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, PREPEND)

    def replace(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REPLACE)

    def update(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, UPDATE)

    def remove(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REMOVE)

    def before(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, BEFORE)

    def after(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, AFTER)


    def _add_target(self, selector, id, action):
        if selector is None != id is None:
            raise ValueError("Either selector or id can be used as a parameter.")
        if selector is None:
            return self.add_target_with_id(id, action)
        return self.add_target_with_selector(selector, action)


    def add_target_with_selector(self, selector, action):
        clone = self._chain()
        clone._targets.append(BroadcastTarget(
            selector_type='css', selector=selector, action=action))
        return clone

    def add_target_with_id(self, selector, action):
        clone = self._chain()
        clone._targets.append(BroadcastTarget(
            selector_type='id', selector=selector, action=action))
        return clone

    def render(self, template, context=None, extra_payload=None):

        if context is None:
            context = dict()

        if extra_payload is None:
            extra_payload = dict()

        channel_layer = get_channel_layer()
        channel_name = get_channel_name(self.stream_name)
        for target in self._targets:
            async_to_sync(channel_layer.group_send)(
                channel_name,
                {
                    "type": self.send_type,
                    "action": target.action,
                    "channel_name": channel_name,
                    "template": template,
                    "context": context,
                    "selector_type": target.selector_type,
                    "selector": target.selector,
                    **extra_payload,
                },
            )
        return self

