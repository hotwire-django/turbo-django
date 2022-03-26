import turbo
from unittest import mock


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
