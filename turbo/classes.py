from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from functools import singledispatchmethod
from django.db.models import Model
from django.template.loader import render_to_string
from .utils import _channel_name_for_instance

# Turbo Streams CRUD operations
APPEND = "append"
PREPEND = "prepend"
REPLACE = "replace"
UPDATE = "update"
REMOVE = "remove"
BEFORE = "before"
AFTER = "after"


class ModelBroadcast:
    def __init__(self, model):
        self.model = model
        super().__init__()
    pass


SELECTOR_CSS = 'css'
SELECTOR_ID = 'id'
SELECTOR_TYPES = (SELECTOR_ID, SELECTOR_CSS)



class Turbo:
    @singledispatchmethod
    def __init__(self, stream_name: str=''):
        self.stream_name = stream_name
        self.stream_target = None

    @singledispatchmethod
    def __init__(self, stream_target: Model):
        self.stream_target = stream_target
        self.stream_name = ''


    def update_stream_name(self):
        # Update the channel name with the stream target's latest pk if needed.
        if self.stream_target:
            self.stream_name = _channel_name_for_instance(self.stream_target)


    def render(self, template_name, context=None) -> "TurboFrame":
        if context is None:
            context = {}

        self.update_stream_name()

        rendered_frame = render_to_string(template_name, context)
        return TurboFrame(self.stream_name, rendered_frame)

    def remove(self, selector=None, id=None):
        """
        Send a broadcast to remove an element from a turbo frame.
        """
        # Remove does not require a template so allow it to pass through without a render().
        self.update_stream_name()
        turboframe = TurboFrame(self.stream_name, '')
        return turboframe.remove(selector=selector, id=id)


class TurboFrame:
    """
    A rendered turbo frame, ready to broadcast.
    """
    def __init__(
        self,
        stream_name: str,
        rendered_template: str='',
    ):
        self.stream_name = stream_name
        self.rendered_template = rendered_template

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
        if selector is None != id is None:
            raise ValueError("Either selector or id can be used as a parameter.")

        selector_type = SELECTOR_CSS
        if selector is None:
            selector_type = SELECTOR_ID
            selector = id

        return self.broadcast(
            self._render_frame(selector_type=selector_type, selector=selector, action=action)
        )


    def _render_frame(self, selector_type, selector, action) -> str:

        template_context = {
            "action": action,
            "use_css_selector": selector_type==SELECTOR_CSS,
            "selector": selector,
        }
        # Remove actions don't have contents, so only add context for model
        # template if it's not a remove action.
        if action != REMOVE:
            template_context["rendered_template"] = self.rendered_template

        rendered_frame = render_to_string("turbo/stream.html", template_context)
        return rendered_frame


    def broadcast(self, rendered_frame):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.stream_name,
            {
                "type": 'notify',
                "channel_name": self.stream_name,
                "rendered_template": rendered_frame
            },
        )
