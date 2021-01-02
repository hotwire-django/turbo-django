from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django.db.models import Model

from turbo import (
    channel_name_for_instance,
    CREATED,
    UPDATED,
    DELETED,
    REPLACE,
    REMOVE,
    APPEND,
)


class BroadcastableMixin(object):
    broadcasts_to = []  # Foreign Key fieldnames to broadcast updates for.
    broadcast_self = True  # Whether or not to broadcast updates on this model's own stream.
    inserts_by = APPEND  # Whether to append or prepend when adding to a list (broadcasting to a foreign key).
    turbo_streams_template = None

    def get_turbo_streams_template(self):
        if self.turbo_streams_template is not None:
            return self.turbo_streams_template
        app_name, model_name = self._meta.label.lower().split(".")
        return f"{app_name}/{model_name}.html"

    def broadcast_to_instance(self, instance, action, to_list, partial=None, context=None):
        if context is None:
            context = dict()
        if partial is None:
            partial = self.get_turbo_streams_template()

        channel_layer = get_channel_layer()
        channel_name = channel_name_for_instance(instance)
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {
                "type": "notify",
                "model": self._meta.label,
                "pk": self.pk,
                "action": action,
                "channel_name": channel_name,
                "template": partial,
                "context": context,
                "to_list": to_list,
            },
        )

    def broadcast(self, model_action):
        if model_action == CREATED:
            streams_action = self.inserts_by
        elif model_action == UPDATED:
            streams_action = REPLACE
        elif model_action == DELETED:
            streams_action = REMOVE
        else:  # TODO: What should the default be?
            streams_action = REPLACE

        if self.broadcast_self:
            self.broadcast_to_instance(self, streams_action, to_list=False)

        for field_name in self.broadcasts_to:
            if hasattr(self, field_name):
                self.broadcast_to_instance(getattr(self, field_name), streams_action, to_list=True)

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        self.broadcast(CREATED if creating else UPDATED)

    def delete(self, *args, **kwargs):
        self.broadcast(DELETED)
        super().delete(*args, **kwargs)
