from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model
from django.template.loader import render_to_string

from typing import Optional

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

    if dom_target is None:
        raise ValueError('Either dom_target or css_selector must be set as a parameter to broadcast_stream().')

    selector_type = "id"
    selector = dom_target

    if dom_target is None:
        selector_type = "css"
        selector = css_selector

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
            "selector_type": selector_type,
            "selector": selector,
            **extra_payload,
        },
    )


class BroadcastTarget:
    def __init__(
        self,
        selector_type,
        selector,
        action,
        template,
        context=None
    ):
        self.selector_type = selector_type
        self.selector = selector
        self.action = action
        self.template = template
        self.context = {}
        self.rendered_context = {}
        if context:
            self.context = context


class Broadcast():

    def __init__(
        self,
        stream_target_name=None,
        stream_name=None,
        send_type='notify'
    ):
        self.stream_target_name = stream_target_name
        if stream_name is None:
            self.stream_name = stream_target_name
        else:
            self.stream_name = stream_name
        self.send_type = send_type
        self.context = dict()
        self._targets = []

    def _chain(self):
        """
        Return a copy of the current Broadcast that's ready for another operation.
        """
        c = self.__class__(stream_target_name=self.stream_target_name)
        c.stream_name = self.stream_name
        c.send_type = self.send_type
        c.context = self.context
        c._targets = self._targets
        return c

    def append(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, APPEND, with_template, context)

    def prepend(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, PREPEND, with_template, context)

    def replace(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REPLACE, with_template, context)

    def update(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, UPDATE, with_template, context)

    def remove(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REMOVE, with_template, context)

    def before(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, BEFORE, with_template, context)

    def after(self, selector=None, id=None, with_template="", context=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, AFTER, with_template, context)


    def _add_target(self, selector, id, action, with_template, context):
        if selector is None != id is None:
            raise ValueError("Either selector or id can be used as a parameter.")
        if selector is None:
            return self.add_target_with_id(id, action, with_template, context)

        return self.add_target_with_selector(selector, action, with_template, context)


    def add_target_with_selector(self, selector, action, with_template, context):
        clone = self._chain()
        clone._targets.append(
            BroadcastTarget(
                selector_type='css', selector=selector, action=action,
                template=with_template, context=context
            )
        )
        return clone

    def add_target_with_id(self, selector, action, with_template, context):
        clone = self._chain()
        clone._targets.append(
            BroadcastTarget(
                selector_type='id', selector=selector, action=action,
                template=with_template, context=context
            )
        )
        return clone

    def set_source_instance(self, instance: Optional[Model]):
        """
        Set the stream_name from the instance
        """
        if instance is None:
            self.stream_name = self.stream_target_name
        else:
            self.stream_name = get_channel_name(instance)


    def _render_template(self, target):

        template_context = {
            "action": target.action,
            "use_css_selector": target.selector_type=='css',
            "selector": target.selector,
        }
        # Remove actions don't have contents, so only add context for model
        # template if it's not a remove action.
        if target.action != REMOVE:
            template_context["model_template"] = target.template

        rendered_context = target.context
        if target.rendered_context:
            rendered_context = target.rendered_context

        print("ct", target.context)
        print("rendered", rendered_context)

        template_context = dict(template_context, **self.context, **rendered_context)
        print(template_context)
        return render_to_string("turbo/stream.html", template_context)


    def broadcast(self):

        channel_layer = get_channel_layer()
        channel_name = self.stream_name
        for target in self._targets:
            async_to_sync(channel_layer.group_send)(
                channel_name,
                {
                    "type": 'notify',
                    "channel_name": channel_name,
                    "rendered_template": self._render_template(target)
                },
            )

