from django import template
from django.core.signing import Signer

from turbo import channel_name_for_instance

register = template.Library()

# https://docs.djangoproject.com/en/3.1/topics/signing/


@register.inclusion_tag('turbo/turbo_stream_source.html')
def turbo_stream_from(model_instance):
    signer = Signer()
    channel_name = channel_name_for_instance(model_instance)
    signed_channel_name = signer.sign(channel_name)
    return {"signed_channel_name": signed_channel_name}
