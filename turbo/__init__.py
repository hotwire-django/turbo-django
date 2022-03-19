# Bring classes up to turbo namespace.
from .classes import (  # noqa: F401
    Stream,
    ModelStream,
    APPEND,
    PREPEND,
    REPLACE,
    UPDATE,
    REMOVE,
    BEFORE,
    AFTER,
    TurboRender,
)
from .module_loading import autodiscover_streams
from .registry import stream_registry
from .shortcuts import render_frame, render_frame_string, remove_frame  # noqa: F401

default_app_config = "turbo.apps.TurboDjangoConfig"


def autodiscover():
    autodiscover_streams(stream_registry)
