from django.db.models import Model

default_app_config = 'turbo.apps.TurboDjangoConfig'


def make_channel_name(model_label, pk):
    return f"BROADCAST-{model_label}-{pk}".lower()


def channel_name_for_instance(instance: Model):
    return make_channel_name(instance._meta.label, instance.pk)


# Model actions
CREATED = "CREATED"
UPDATED = "UPDATED"
DELETED = "DELETED"

# Turbo Streams CRUD operations
APPEND = "append"
PREPEND = "prepend"
REPLACE = "replace"
REMOVE = "remove"
