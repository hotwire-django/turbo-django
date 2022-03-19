import turbo


def test_tests():
    assert True


def test_import():
    assert turbo.default_app_config == "turbo.apps.TurboDjangoConfig"


class TestChannel(turbo.Stream):
    class Meta:
        app_name = 'test'

    pass


def test_channel_name():

    assert TestChannel.channel_name == "test:TestChannel"
    pass
