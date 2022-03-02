from django.utils.module_loading import autodiscover_modules
from django.db.models.signals import post_init, post_save, post_delete

import sys
from inspect import getmembers, isclass

from .classes import Channel, ModelChannel  # noqa: F401
from turbo.signals import (
    post_save_broadcast_model,
    post_delete_broadcast_model,
    post_init_broadcast_model,
)


def autodiscover_channels(register_to):
    """
    Add all Channels to registry
    Look for ModelChannel classes in channels.py
    """
    autodiscover_modules("channels")
    broadcast_modules = [v for k, v in sys.modules.items() if k.endswith(".channels")]

    for broadcast_module in broadcast_modules:
        app_name = broadcast_module.__package__

        channels = [x for x in getmembers(broadcast_module, isclass) if issubclass(x[1], Channel)]
        # wrap model channels with signals and assign _meta attribute
        for channel_model_name, channel_model in channels:
            channel_model._meta.app_name = app_name
            if issubclass(channel_model, ModelChannel):
                try:
                    model = channel_model._meta.model
                except (KeyError, AttributeError):
                    raise AttributeError(f"{channel_model.__name__} missing Meta.model attribute")

                model._meta.channel_model = channel_model
                post_init.connect(post_init_broadcast_model, sender=model)
                post_save.connect(post_save_broadcast_model, sender=model)
                post_delete.connect(post_delete_broadcast_model, sender=model)

            register_to.add_channel(app_name, channel_model_name, channel_model)
