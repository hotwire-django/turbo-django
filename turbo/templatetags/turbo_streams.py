from django import template
from django.core.signing import Signer
from django.db.models import Model

from turbo import get_channel_name

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_stream_from(model_instance):
    # https://docs.djangoproject.com/en/3.1/topics/signing/
    signer = Signer()
    channel_name = get_channel_name(model_instance)
    signed_channel_name = signer.sign(channel_name)
    return {"signed_channel_name": signed_channel_name}


@register.simple_tag
def stream_id(target):
    if isinstance(target, Model):
        model_instance: Model = target
        model_name = model_instance._meta.verbose_name.lower()
        pk = model_instance.pk
        return f"{model_name}_{pk}"
    else:
        return f"{target.__str__().lower()}"
