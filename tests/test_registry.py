import turbo

from turbo.classes import Stream
from turbo.registry import stream_for_stream_name, stream_registry


class TestStream(turbo.Stream):
    pass


def test_registry_invalid_names():

    # test invalid stream names
    assert stream_for_stream_name('') is None
    assert stream_for_stream_name('a') is None


def test_registry_add_stream():

    # test stream before it is added to the registry
    assert stream_for_stream_name('test_app:TestStream') is None

    # test stream after it is added to the registry
    stream_registry.add_stream('test_app', 'TestStream', TestStream)
    assert stream_for_stream_name('test_app:TestStream') is TestStream

    assert stream_registry.get_stream_names() == [":TestStream"]
