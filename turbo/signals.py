def post_init_broadcast_model(sender, instance, **kwargs):
    if hasattr(sender._meta, "stream_model"):
        instance.stream = sender._meta.stream_model.from_instance(instance)


def post_save_broadcast_model(sender, instance, **kwargs):
    if hasattr(instance.stream, "on_save"):
        instance.stream.on_save(instance, **kwargs)


def post_delete_broadcast_model(sender, instance, **kwargs):
    if hasattr(instance.stream, "on_delete"):
        instance.stream.on_delete(instance, **kwargs)
