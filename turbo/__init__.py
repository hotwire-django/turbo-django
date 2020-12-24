default_app_config = 'turbo.apps.TurboDjangoConfig'


def get_broadcast_channel(model, stream, value):
    return f"BROADCAST-{model}-{stream}-{value}"
