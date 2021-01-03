from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model

from turbo import (
    get_channel_name,
    CREATED,
    UPDATED,
    DELETED,
    REPLACE,
    REMOVE,
    APPEND,
)


class BroadcastableMixin(object):
    default_stream_action = APPEND
    broadcasts_to = []  # Foreign Key fieldnames to broadcast updates for.
    turbo_streams_template = None

    def get_turbo_streams_template(self, target):
        raise NotImplementedError

    def _get_context(self, target):
        context = {"model_template": self.get_turbo_streams_template(target)}
        context.update(self.append_context(target))
        return context

    def append_context(self, target):
        return {}

    def send_broadcast(self, target, action, partial=None):
        if partial is None:
            partial = self.get_turbo_streams_template(target)

        channel_layer = get_channel_layer()
        channel_name = get_channel_name(target)
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {
                "type": "notify",
                "action": action,
                "channel_name": channel_name,
                "template": partial,
                "context": self._get_context(target),
                "dom_target": self.get_dom_target(target),
            },
        )

    def broadcast(self, stream_action=None):
        if stream_action is None:
            stream_action = self.default_stream_action
        for channel_name in self.broadcasts_to:
            self.send_broadcast(channel_name, stream_action)

    def get_dom_target(self, target):
        return None


class BroadcastableModelMixin(BroadcastableMixin):
    broadcast_self = True  # Whether or not to broadcast updates on this model's own stream.
    inserts_by = APPEND  # Whether to append or prepend when adding to a list (broadcasting to a foreign key).

    def get_turbo_streams_template(self, target):
        if self.turbo_streams_template is not None:
            return self.turbo_streams_template
        app_name, model_name = self._meta.label.lower().split(".")
        return f"{app_name}/{model_name}.html"

    def append_context(self, target):

        # Add Custom context
        app_name, model_name = self._meta.label.lower().split(".")
        return {
            "object": self,
            model_name: self
        }

    def get_action(self, model_action):
        if model_action == CREATED:
            streams_action = self.inserts_by
        elif model_action == UPDATED:
            streams_action = REPLACE
        elif model_action == DELETED:
            streams_action = REMOVE
        else:  # TODO: What should the default be?
            streams_action = REPLACE
        return streams_action

    def broadcast(self, model_action):
        streams_action = self.get_action(model_action)

        if self.broadcast_self:
            self.send_broadcast(self, streams_action)

        for field_name in self.broadcasts_to:
            if hasattr(self, field_name):
                self.send_broadcast(getattr(self, field_name), streams_action)
            else:
                self.send_broadcast(field_name, streams_action)

    def get_dom_target(self, target):
        if isinstance(target, Model):
            model: Model = target
            if self._meta.model != model:
                # Broadcast to self
                return self._meta.verbose_name_plural.lower()
            else:
                return f"{self._meta.verbose_name.lower()}_{self.pk}"
        else:
            return f'{target.lower()}'

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        self.broadcast(CREATED if creating else UPDATED)

    def delete(self, *args, **kwargs):
        self.broadcast(DELETED)
        super().delete(*args, **kwargs)
