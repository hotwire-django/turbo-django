from collections import defaultdict
import re
import logging

from .classes import Stream


logger = logging.getLogger("turbo.streams")

model_stream_regex = re.compile(r"(?P<app_name>\w+)\.(?P<app_name2>\w+)\.(?P<stream_name>\w+)(\-(?P<pk>[\w-]+))?")
# stream_regex = re.compile(r"(?P<app_name>\w+)\:(?P<stream_name>\w+)")


class StreamRegistry(dict):

    streams_by_app = defaultdict(dict)

    def add_stream(self, app_name, stream_name, stream):
        self.streams_by_app[app_name][stream_name] = stream

    def get_stream(self, app_name: str, stream_name: str) -> Stream:
        return self.streams_by_app[app_name].get(stream_name)

    def get_stream_names(self):
        stream_names = []
        for app, streams in self.streams_by_app.items():
            for stream in streams.values():
                stream_names.append(stream.stream_name)
        return stream_names


def stream_for_stream_name(stream_name: str):
    """
    Parses a stream name and returns either the stream or
    all streams that are associated with the instance.


    >>> stream_for_stream_name("app:RegularStream")
    >>> stream_for_stream_name("app:ModelChanel")
    (Stream, is_model_stream, pk)
    """
    stream_parts = stream_regex.match(stream_name)
    if not stream_parts:
        logger.warning("Stream '%s' could not be parsed.", stream_name)
        # changed
        return None, {}, None

    StreamCls = stream_registry.get_stream(
        f"{model_stream_parts['app_name']}.{model_stream_parts['app_name2']}", model_stream_parts["stream_name"]
    )
    is_model_stream = False
    if StreamCls:
        is_model_stream = issubclass(StreamCls, ModelStream)
    return (StreamCls, is_model_stream, model_stream_parts["pk"])
    #     return None

    # StreamCls = stream_registry.get_stream(stream_parts["app_name"], stream_parts["stream_name"])

    # return StreamCls


stream_registry = StreamRegistry()
