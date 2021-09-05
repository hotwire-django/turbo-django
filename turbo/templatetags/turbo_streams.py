from django import template
from django.core.signing import Signer
from django.db.models import Model

from turbo import get_channel_name

register = template.Library()


@register.inclusion_tag("turbo/turbo_stream_source.html")
def turbo_subscribe(*stream_names):
    # https://docs.djangoproject.com/en/3.1/topics/signing/
    signer = Signer()
    signed_channel_names = [signer.sign(get_channel_name(s)) for s in stream_names]
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
