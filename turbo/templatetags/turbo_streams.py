from django import template
from django.core.signing import Signer
from django.db.models import Model
from django.template import (
    TemplateSyntaxError,
)

from turbo.registry import channel_for_channel_name
from turbo.utils import to_subscribable_name

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_subscribe(*stream_items):
    # https://docs.djangoproject.com/en/3.1/topics/signing/
    channel_names = []
    signed_channel_names = []

    signer = Signer()
    for stream_item in stream_items:

        if isinstance(stream_item, Model):
            channel = stream_item.channel
        else:
            channel, is_model_channel, pk = channel_for_channel_name(
                to_subscribable_name(stream_item)
            )
            if is_model_channel:
                channel = Channel.from_pk(pk)

            if not channel:
                raise TemplateSyntaxError('Could not fetch channel with name: %s' % stream_item)
                continue

        channel_names.append(channel.channel_name)

    signed_channel_names = [signer.sign(to_subscribable_name(s)) for s in channel_names]
    return {"signed_channel_names": signed_channel_names}


# deprecated - used in version 0.1.0
@register.simple_tag
def stream_id(target):
    if isinstance(target, Model):
        model_instance: Model = target
        model_name = model_instance._meta.verbose_name.lower()
        pk = model_instance.pk
        return f"{model_name}_{pk}"
    else:
        return f"{target.__str__().lower()}"
