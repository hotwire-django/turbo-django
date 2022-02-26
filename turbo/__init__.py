from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Bring classes up to turbo namespace.

from .classes import (  # noqa: F401
    Channel,
    ModelChannel,
    APPEND,
    PREPEND,
    REPLACE,
    UPDATE,
    REMOVE,
    BEFORE,
    AFTER,
    TurboRender
)
from .module_loading import autodiscover_channels
from .registry import channel_registry
from .shortcuts import render_frame, render_frame_string, remove_frame


default_app_config = "turbo.apps.TurboDjangoConfig"

from django.contrib.admin.sites import AdminSite, site



def autodiscover():
   autodiscover_channels(channel_registry)
