from django.utils.module_loading import autodiscover_modules
from django.db.models.signals import post_init, post_save, post_delete

import sys
from inspect import getmembers, isclass

from .classes import Stream, ModelStream  # noqa: F401
from turbo.signals import (
    post_save_broadcast_model,
    post_delete_broadcast_model,
    post_init_broadcast_model,
)


def autodiscover_streams(register_to):
    """
    Add all Streams to registry
    Look for ModelStream classes in streams.py
    """
    autodiscover_modules("streams")
    broadcast_modules = [v for k, v in sys.modules.items() if k.endswith(".streams")]

    for broadcast_module in broadcast_modules:
        app_name = broadcast_module.__package__

        streams = [x for x in getmembers(broadcast_module, isclass) if issubclass(x[1], Stream)]
        # wrap model streams with signals and assign _meta attribute
        for stream_model_name, stream_model in streams:
            stream_model._meta.app_name = app_name
            if issubclass(stream_model, ModelStream):
                try:
                    model = stream_model._meta.model
                except (KeyError, AttributeError):
                    raise AttributeError(f"{stream_model.__name__} missing Meta.model attribute")

                model._meta.stream_model = stream_model
                post_init.connect(post_init_broadcast_model, sender=model)
                post_save.connect(post_save_broadcast_model, sender=model)
                post_delete.connect(post_delete_broadcast_model, sender=model)

            register_to.add_stream(app_name, stream_model_name, stream_model)
