from django.db.models import Model
from collections import Iterable

import turbo
from turbo import (
    CREATED,
    UPDATED,
    DELETED,
    REPLACE,
    REMOVE,
    APPEND,
)

class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.  """

    def __init__(self, init={}):
        dict.__init__(self, init)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        return super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, name):
        return super(AttrDict, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AttrDict, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

def assign_meta(new_class, bases, meta):
    m = {}
    for base in bases:
        m.update({k: v for k, v in getattr(base, "_broadcast", {}).items()})

    m.update({k: v for k, v in getattr(meta, "__dict__", {}).items() if not k.startswith("__")})

    _broadcast = AttrDict(m)

    return _broadcast

class BroadcastMetaclass(type(Model)):
    """
    Metaclass that collects Fields declared on the base classes.
    """
    def __new__(mcs, name, bases, attrs):

        # Pop the Broadcast class if exists
        broadcast_inner_obj = attrs.pop('Broadcast', None)
        new_class = (super().__new__(mcs, name, bases, attrs))

        _broadcast = assign_meta(new_class, bases, broadcast_inner_obj)

        new_class._broadcast = _broadcast

        return new_class


class BroadcastableMixin(object, metaclass=BroadcastMetaclass):

    class Broadcast:

        def __init__(self):
            self._broadcast = {
                "on_save": (),
                "on_create" : (),
                "on_update" : (),
                "on_delete" : (),
            }

    def broadcast(self, broadcast: turbo.Broadcast):
        if broadcast.stream_target_name == "self":
            broadcast.set_source_instance(self)

        elif hasattr(self, broadcast.stream_target_name):
            broadcast.set_source_instance(getattr(self, broadcast.stream_target_name))
        else:
            broadcast.set_source_instance(None)

        for target in broadcast._targets:
            target.rendered_context = self._process_context(target.context)

        broadcast.broadcast()

    def _process_context(self, context):
        rendered_context = {}
        for k, v in context.items():
            if v == "self":
                rendered_context[k] = self
            else:
                rendered_context[k] = v

        return rendered_context

    def get_dom_target(self, target):
        if isinstance(target, Model):
            model: Model = target
            if self._meta.model != model:
                # Broadcast to self
                return self._meta.verbose_name_plural.lower()
            else:
                return f"{self._meta.verbose_name.lower()}_{self.pk}"
        else:
            return f"{target.lower()}"

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        for b in self._broadcast.get('on_save', ()):
            self.broadcast(b)

        if creating:
            for b in self._broadcast.get('on_create', ()):
                self.broadcast(b)
        else:
            for b in self._broadcast.get('on_update', ()):
                self.broadcast(b)

    def delete(self, *args, **kwargs):
        for b in self._broadcast.get('on_delete', ()):
            self.broadcast(b)
        super().delete(*args, **kwargs)
