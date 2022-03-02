from collections import defaultdict
import re
import logging

from .classes import Channel, ModelChannel


logger = logging.getLogger("turbo.channels")

model_channel_regex = re.compile(r"(?P<app_name>\w+)\.(?P<channel_name>\w+)(\-(?P<pk>[\w-]+))?")


class ChannelRegistry(dict):

    channels_by_app = defaultdict(dict)

    def add_channel(self, app_name, channel_name, channel):
        self.channels_by_app[app_name][channel_name] = channel

    def get_channel(self, app_name: str, channel_name: str) -> Channel:
        return self.channels_by_app[app_name].get(channel_name)


def channel_for_channel_name(channel_name: str):
    """
    Parses a channel name and returns either the channel or
    all channels that are associated with the instance.


    >>> channel_for_channel_name("app.RegularChannel")
    >>> channel_for_channel_name("app.ModelChanel-1")
    (Channel, is_model_channel, pk)
    """
    model_channel_parts = model_channel_regex.match(channel_name)

    if not model_channel_parts:
        logger.warning("Channel '%s' could not be parsed.", channel_name)
        return None, {}, None

    ChannelCls = channel_registry.get_channel(
        model_channel_parts["app_name"], model_channel_parts["channel_name"]
    )
    is_model_channel = False
    if ChannelCls:
        is_model_channel = issubclass(ChannelCls, ModelChannel)
    return (ChannelCls, is_model_channel, model_channel_parts["pk"])


channel_registry = ChannelRegistry()
