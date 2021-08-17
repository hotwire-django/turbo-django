from django.db.models.signals import post_save, post_delete


def register(*models, site=None):
    """
    Register the given model(s) classes with the ModelBroadcast.
    This attaches the on_save and on_delete methods to the provided
    model signals.

    .. code-block:: python

        @turbo.register(Room)
        class RoomBroadcast(turbo.ModelBroadcast):

            def on_save(self, room, created, *args, **kwargs):
                    pass

            def on_delete(self, room, *args, **kwargs):
                    pass

    """
    from turbo.classes import ModelBroadcast

    def _model_broadcast_wrapper(broadcast_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        if not issubclass(broadcast_class, ModelBroadcast):
            raise ValueError('Wrapped class must subclass ModelBroadcast.')

        for model in models:
            model.broadcast_class = broadcast_class(model)
            post_save.connect(post_save_broadcast_model, sender=model)
            post_delete.connect(post_delete_broadcast_model, sender=model)

        return broadcast_class

    return _model_broadcast_wrapper


def post_save_broadcast_model(sender, instance, **kwargs):
    if hasattr(sender.broadcast_class, 'on_save'):
        sender.broadcast_class.on_save(instance, kwargs)


def post_delete_broadcast_model(sender, instance, **kwargs):
    if hasattr(sender.broadcast_class, 'on_delete'):
        sender.broadcast_class.on_delete(instance, kwargs)
