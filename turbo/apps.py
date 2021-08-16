from django.apps import AppConfig


class TurboDjangoConfig(AppConfig):
    """The default AppConfig for admin which does autodiscovery."""

    name = "turbo"

    def ready(self):
        super().ready()
        self.module.autodiscover()
