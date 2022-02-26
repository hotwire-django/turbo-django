from django.db.models import Model


def to_subscribable_name(channel_name):
    return channel_name.__str__().replace(":", ".")
