from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from functools import cached_property

from django.http import HttpResponse
from django.template.loader import render_to_string

from .utils import to_subscribable_name
from .metaclass import DeclarativeFieldsMetaclass

# Turbo Streams CRUD operations
APPEND = "append"
PREPEND = "prepend"
REPLACE = "replace"
UPDATE = "update"
REMOVE = "remove"
BEFORE = "before"
AFTER = "after"


SELECTOR_CSS = "css"
SELECTOR_ID = "id"
SELECTOR_TYPES = (SELECTOR_ID, SELECTOR_CSS)


class classproperty:
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class Channel(metaclass=DeclarativeFieldsMetaclass):
    """
    A reference to a specific broadcast.
    """

    class Meta:
        app_name = ""

    @classproperty
    def channel_name(self):
        return f"{self._meta.app_name}:{self.__name__}"

    @property
    def label(self):
        return "%s.%s" % (self.app_label, self.object_name)

    def _get_frame(self, template=None, context=None, text=None):
        if text:
            return TurboRender(text)
        else:
            return TurboRender.init_from_template(template, context)

    def append(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""

        frame = self._get_frame(template, context, text)
        frame.append(selector=selector, id=id)
        self.stream(frame)

    def prepend(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""
        frame = self._get_frame(template, context, text)
        frame.prepend(selector=selector, id=id)
        self.stream(frame)

    def replace(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""
        frame = self._get_frame(template, context, text)
        frame.replace(selector=selector, id=id)
        self.stream(frame)

    def update(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""
        frame = self._get_frame(template, context, text)
        frame.update(selector=selector, id=id)
        self.stream(frame)

    def before(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""
        frame = self._get_frame(template, context, text)
        frame.before(selector=selector, id=id)
        self.stream(frame)

    def after(self, template=None, context=None, text=None, selector=None, id=None):
        """Shortcut to stream an append frame"""
        frame = self._get_frame(template, context, text)
        frame.after(selector=selector, id=id)
        self.stream(frame)

    def remove(self, selector=None, id=None):
        """
        Send a broadcast to remove an element from a turbo frame.
        """
        # Remove does not require a template so allow it to pass through without a render().
        remove_frame = TurboRender().remove(selector, id)
        self.stream(remove_frame)

    def stream_raw(self, raw_text: str):
        channel_layer = get_channel_layer()
        subscribable_stream_name = to_subscribable_name(self.channel_name)

        async_to_sync(channel_layer.group_send)(
            subscribable_stream_name,
            {
                "type": "notify",
                "channel_name": subscribable_stream_name,
                "rendered_template": raw_text,
            },
        )

    def stream(self, frame: "TurboRender"):
        if not frame.rendered_template:
            raise ValueError("No action (append, update, remove...) assigned to Turbo Frame.")
        self.stream_raw(frame.rendered_template)

    def user_passes_test(self, user):
        return True


class ModelChannel(Channel):
    def __init__(self, pk, instance=None):
        super().__init__()
        self.pk = pk
        if instance:
            self.instance = instance

    @classmethod
    def from_pk(cls, pk):
        return cls(pk, None)

    @classmethod
    def from_instance(cls, instance):
        return cls(instance.pk, instance)

    @cached_property
    def instance(self):
        return self._meta.model.objects.get(pk=self.pk)

    @property
    def channel_name(self):
        return f"{super().channel_name}-{self.pk}"

    def user_passes_test(self, user):
        return True

    # Optionally defined in inherited classes
    #
    # def on_save(self, instance, created, *args, **kwargs):
    #     pass

    # def on_delete(self, instance, *args, **kwargs):
    #     pass


class TurboRender:
    """
    A rendered template, ready to broadcast using turbo.
    """

    def __init__(self, inner_html: str = ""):
        self.inner_html = inner_html
        self._rendered_template = None

    @classmethod
    def init_from_template(cls, template_name: str, context=None, request=None) -> "TurboRender":
        """
        Returns a TurboRender object from a django template.  This rendered template
        can then be broadcast to subscribers with the TurboRender actions
        (eg: append, update, etc...)

        Takes a template name and context identical to Django's render() method.
        """
        if context is None:
            context = {}

        return cls(render_to_string(template_name, context, request))

    def append(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, APPEND)

    def prepend(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, PREPEND)

    def replace(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REPLACE)

    def update(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, UPDATE)

    def remove(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, REMOVE)

    def before(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, BEFORE)

    def after(self, selector=None, id=None):
        """Add a target action to the given selector."""
        return self._add_target(selector, id, AFTER)

    def _add_target(self, selector, id, action):

        if (selector is None) == (id is None):  # noqa: E711
            raise ValueError("Either selector or id can be used as a parameter.")

        selector_type = SELECTOR_CSS
        if selector is None:
            selector_type = SELECTOR_ID
            selector = id

        return self.render(selector_type=selector_type, selector=selector, action=action)

    @property
    def response(self):
        return HttpResponse(self.rendered_template, "text/vnd.turbo-stream.html", 200)

    @property
    def rendered_template(self):
        if self._rendered_template is None:
            raise ValueError(
                "Template must be rendered with an template action (append, update, remove, etc...)"
            )
        return self._rendered_template

    def render(self, selector_type, selector, action) -> str:

        template_context = {
            "action": action,
            "use_css_selector": selector_type == SELECTOR_CSS,
            "selector": selector,
        }

        # Remove actions don't have contents, so only add context for model
        # template if it's not a remove action.
        if action != REMOVE:
            template_context["rendered_template"] = self.inner_html

        self._rendered_template = render_to_string("turbo/stream.html", template_context)
        return self

    def stream_to(self, channel):
        channel.stream(self.rendered_template)
