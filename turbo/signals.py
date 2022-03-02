def post_init_broadcast_model(sender, instance, **kwargs):
    if hasattr(sender._meta, "channel_model"):
        instance.channel = sender._meta.channel_model.from_instance(instance)


def post_save_broadcast_model(sender, instance, **kwargs):
    if hasattr(instance.channel, "on_save"):
        instance.channel.on_save(instance, **kwargs)


def post_delete_broadcast_model(sender, instance, **kwargs):
    if hasattr(instance.channel, "on_delete"):
        instance.channel.on_delete(instance, **kwargs)
