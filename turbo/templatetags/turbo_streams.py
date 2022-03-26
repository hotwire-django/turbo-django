from django import template
from django.core.signing import Signer
from django.db.models import Model
from django.template import (
    TemplateSyntaxError,
)

from turbo.registry import stream_for_stream_name, stream_registry
from turbo.utils import to_subscribable_name

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_subscribe(*stream_items):
    # https://docs.djangoproject.com/en/3.1/topics/signing/
    stream_names = []
    signed_stream_names = []

    signer = Signer()
    for stream_item in stream_items:

        if isinstance(stream_item, Model):
            stream = stream_item.stream
        else:
            Stream, is_model_stream, pk = stream_for_stream_name(to_subscribable_name(stream_item))

            if not Stream:
                stream_names = stream_registry.get_stream_names()
                raise TemplateSyntaxError(
                    "Could not fetch stream with name: '%s'  Registered streams: %s"
                    % (stream_item, stream_names)
                )
                continue

            if is_model_stream:
                stream = Stream.from_pk(pk)
            else:
                stream = Stream()

        stream_names.append(stream.stream_name)
    signed_stream_names = [signer.sign(to_subscribable_name(s)) for s in stream_names]
    return {"signed_channel_names": signed_stream_names}
