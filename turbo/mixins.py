from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from turbo import channel_name_for_instance


class BroadcastableMixin(object):
    broadcasts_to = []  # Foreign Key fieldnames to broadcast updates for.
    broadcast_self = True  # Whether or not to broadcast updates on this model's own stream.
    inserts_by = "append"  # Whether to append or prepend when adding to a list (broadcasting to a foreign key).
    turbo_streams_template = None

    def get_turbo_streams_template(self):
        if self.turbo_streams_template is not None:
            return self.turbo_streams_template
        app_name, model_name = self._meta.label.lower().split(".")
        return f"{app_name}/{model_name}.html"

    def broadcast_to_instance(self, instance, action, partial=None, context=None):
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
            })

    def broadcast(self, created):
        action = self.inserts_by if created else "replace"
        if self.broadcast_self:
            self.broadcast_to_instance(self, "replace")

        for field_name in self.broadcasts_to:
            if hasattr(self, field_name):
                self.broadcast_to_instance(getattr(self, field_name), action)

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        self.broadcast(creating)
