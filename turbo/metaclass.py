class AttrDict(dict):
    """A dictionary with attribute-style access. It maps attribute access to
    the real dictionary."""

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

    def __dir__(self):
        """Replace dict autocomplete choices with dict keys"""
        return self.keys()

    __getattr__ = __getitem__
    __setattr__ = __setitem__


def assign_meta(new_class, bases, meta):
    m = {}
    for base in bases:
        m.update({k: v for k, v in getattr(base, "_meta", {}).items()})

    m.update({k: v for k, v in getattr(meta, "__dict__", {}).items() if not k.startswith("__")})
    _meta = AttrDict(m)

    return _meta


class DeclarativeFieldsMetaclass(type):
    """
    Metaclass that updates a _meta dict declared on base classes.
    """

    def __new__(mcs, name, bases, attrs):

        # Pop the Meta class if exists
        meta = attrs.pop("Meta", None)

        # Value of abstract by default should be set to false.
        # It is never inherited.
        abstract = getattr(meta, "abstract", False)

        new_class = super().__new__(mcs, name, bases, attrs)

        _meta = assign_meta(new_class, bases, meta)

        _meta.abstract = abstract

        new_class._meta = _meta

        return new_class
