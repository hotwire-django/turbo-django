from django import template
from django.db.models import Model
from django.template import (
    TemplateSyntaxError,
)

from turbo.registry import stream_for_stream_name, stream_registry
from turbo.classes import Stream

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_subscribe(*stream_items):
    stream_names = []
    streams = []

    for stream_item in stream_items:

        if isinstance(stream_item, Model):
            stream = stream_item.stream
        elif isinstance(stream_item, Stream):
            stream = stream_item
        else:
            StreamClass = stream_for_stream_name(stream_item)

            if not StreamClass:
                stream_names = stream_registry.get_stream_names()
                raise TemplateSyntaxError(
                    "Could not fetch stream with name: '%s'  Registered streams: %s"
                    % (stream_item, stream_names)
                )
                continue
            stream = StreamClass()
        streams.append(stream)

    return {"streams": streams}


@register.inclusion_tag("turbo/components/broadcast_component.html", takes_context=True)
def turbo_component(context, component, *args, **kwargs):
    if isinstance(component, str):
        # figure out component from the string
        ComponentClass = stream_for_stream_name(component)
        component = ComponentClass(*args, **kwargs)

    initial_render = component.initial_render(context.flatten())
    return {"component": component, "initial_render": initial_render}
