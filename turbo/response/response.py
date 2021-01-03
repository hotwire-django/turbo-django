# Django
from django.http import HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse

# Local
from .renderers import render_turbo_frame, render_turbo_stream, Action
from .. import send_broadcast
from ..mixins import Broadcastable


class TurboStreamResponseMixin:
    """Automatically sets the correct turbo-stream content type."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            content_type="text/html; turbo-stream; charset=utf-8", *args, **kwargs
        )


class TurboStreamStreamingResponse(TurboStreamResponseMixin, StreamingHttpResponse):
    """Handles turbo-stream responses. Generator should yield individual
    turbo-stream strings."""


class TurboStreamResponse(Broadcastable, TurboStreamResponseMixin, HttpResponse):
    """Basic turbo-stream response."""

    def __init__(self, content="", *, action, target, **kwargs):
        super().__init__(
            render_turbo_stream(action, target, content), **kwargs,
        )
        self._action = action
        self._target = target

    def broadcast(self, target):
        send_broadcast(target, self._target, self._action, data=self.content.decode('utf-8'))


class TurboStreamTemplateResponse(Broadcastable, TurboStreamResponseMixin, TemplateResponse):
    """Handles turbo-stream template response.

    Adds the following variables to the template:

    - **is_turbo_stream**
    - **turbo_stream_action**
    - **turbo_stream_target**

    """

    is_turbo_stream = True

    def __init__(self, request, template, context, *, action: Action, target, **kwargs):
        super().__init__(
            request,
            template,
            {
                **context,
                "turbo_stream_action": action.value,
                "turbo_stream_target": target,
                "is_turbo_stream": True,
            },
            **kwargs,
        )

        self._target = target
        self._action = action

    @property
    def rendered_content(self):
        return render_turbo_stream(
            action=self._action, target=self._target, content=super().rendered_content
        )

    def broadcast(self, target):
        send_broadcast(target, self._target, self._action, data=self.rendered_content)


class TurboFrameResponse(HttpResponse):
    """Handles turbo-frame template response."""

    def __init__(self, content=b"", *, dom_id, **kwargs):
        super().__init__(
            render_turbo_frame(dom_id, content), **kwargs,
        )


class TurboFrameTemplateResponse(TemplateResponse):
    """Handles turbo-stream template response.

    Adds the following variables to the template:

    - **is_turbo_frame**
    - **turbo_frame_dom_id**

    """

    is_turbo_frame = True

    def __init__(self, request, template, context, *, dom_id, **kwargs):
        super().__init__(
            request,
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        )

        self._dom_id = dom_id

    @property
    def rendered_content(self):
        return render_turbo_frame(self._dom_id, super().rendered_content)
