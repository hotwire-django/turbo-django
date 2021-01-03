from django import template
from django.core.signing import Signer

from turbo import channel_name_for_instance

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_stream_from(model_instance):
    # https://docs.djangoproject.com/en/3.1/topics/signing/
    signer = Signer()
    channel_name = channel_name_for_instance(model_instance)
    signed_channel_name = signer.sign(channel_name)
    return {"signed_channel_name": signed_channel_name}


@register.inclusion_tag("turbo/turbo_stream_id.html")
def stream_id(model_instance):
    model_name = model_instance._meta.verbose_name.lower()
    pk = model_instance.pk
    return {"dom_id": f"{model_name}_{pk}"}
