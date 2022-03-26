from . import context
import turbo


def test_tests():
    assert True


def test_import():
    assert turbo.default_app_config == "turbo.apps.TurboDjangoConfig"
