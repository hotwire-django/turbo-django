from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from turbo import get_broadcast_channel


class BroadcastableMixin(object):

    def get_streams(self):
        """
        Allow subscribing to streams for objects by their primary key (single updates),
        or any ForeignKey present on the model.
        """
        streams = ["pk"]
        for field in self._meta.get_fields():
            if field.get_internal_type() == 'ForeignKey':
                streams.append(field.get_attname())
        return streams

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        action = "CREATE" if self._state.adding else "UPDATE"
        super().save(*args, **kwargs)
        for stream in self.get_streams():
            if hasattr(self, stream):
                channel = get_broadcast_channel(self._meta.label.lower(), stream, getattr(self, stream))
                print(f"SENDING ON {channel}")
                async_to_sync(channel_layer.group_send)(
                    channel,
                    {
                        "type": "notify",
                        "model": self._meta.label,
                        "pk": self.pk,
                        "stream": stream,
                        "action": action,
                        "channel": channel,
                    })
