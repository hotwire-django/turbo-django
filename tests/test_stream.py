import turbo
from unittest import mock

from turbo.classes import Stream


def test_tests():
    assert True


def test_import():
    assert turbo.default_app_config == "turbo.apps.TurboDjangoConfig"


class TestStream(turbo.Stream):
    pass


@mock.patch("turbo.classes.async_to_sync")
def test_stream(async_to_sync):
    stream = TestStream()
    assert stream.stream_name == ':TestStream'

    stream.append(text="Hi", id="id_of_object")
    async_to_sync.assert_called_once()


@mock.patch.object(Stream, "stream_raw")
def test_stream_actions(stream_raw):
    stream = TestStream()
    assert stream.stream_name == ':TestStream'

    actions = ('append', 'prepend', 'replace', 'update', 'before', 'after')
    for action_name in actions:
        action_method = getattr(stream, action_name)
        action_method(text="Hi", id="id_of_object")

        assert stream_raw.call_count == 1
        args = stream_raw.mock_calls[0].args
        assert args == (
            f'<turbo-stream action="{action_name}" target="id_of_object"><template>Hi</template></turbo-stream>',
        )
        stream_raw.reset_mock()


@mock.patch.object(Stream, "stream_raw")
def test_stream_remove(stream_raw):
    stream = TestStream()
    assert stream.stream_name == ':TestStream'

    actions = ('append', 'prepend', 'replace', 'update', 'before', 'after')

    stream.remove(id="id_of_object")

    assert stream_raw.call_count == 1
    args = stream_raw.mock_calls[0].args
    assert args == (
        '<turbo-stream action="remove" target="id_of_object"><template></template></turbo-stream>',
    )
