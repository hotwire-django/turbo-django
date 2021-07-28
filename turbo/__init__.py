from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Model
from django.template.loader import render_to_string

from typing import Optional

default_app_config = "turbo.apps.TurboDjangoConfig"

from .classes import (
    ModelBroadcast,
    APPEND, PREPEND, REPLACE, UPDATE, REMOVE, BEFORE, AFTER,
)
from .utils import get_channel_name

from turbo.decorators import register
from django.contrib.admin.sites import site
from django.utils.module_loading import autodiscover_modules


def autodiscover():
    """
    Look for ModelBroadcast classes in broadcasts.py
    """
    autodiscover_modules('broadcasts')


def broadcast_stream(
    stream_target,
    action,
    template,
    context,
    dom_target=None,
    css_selector=None,
    send_type="notify",
    extra_payload=None,
):
    """
    Send a Broadcast to all Websocket Clients registered to a specific stream!
    """
    if extra_payload is None:
        extra_payload = dict()

    if dom_target is None:
        raise ValueError('Either dom_target or css_selector must be set as a parameter to broadcast_stream().')

    selector_type = "id"
    selector = dom_target

    if dom_target is None:
        selector_type = "css"
        selector = css_selector

    channel_layer = get_channel_layer()
    channel_name = get_channel_name(stream_target)
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            "type": send_type,
            "action": action,
            "channel_name": channel_name,
            "template": template,
            "context": context,
            "selector_type": selector_type,
            "selector": selector,
            **extra_payload,
        },
    )

