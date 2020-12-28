from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from turbo import channel_name_for_instance


class BroadcastableMixin(object):
    broadcast_to = []  # Foreign Key fieldnames to broadcast updates for.
    broadcast_self = True  # Whether or not to broadcast updates on this model's own stream.
    inserts_by = "append"  # Whether to append or prepend when adding to a list (broadcasting to a foreign key).

    def _broadcast_to_instance(self, instance, action):
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
            })

    def save(self, *args, **kwargs):
        action = self.inserts_by if self._state.adding else "replace"
        super().save(*args, **kwargs)
        if self.broadcast_self:
            self._broadcast_to_instance(self, "replace")

        for field_name in self.broadcast_to:
            if hasattr(self, field_name):
                self._broadcast_to_instance(getattr(self, field_name), action)

