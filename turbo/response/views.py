# Django
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)

# Local
from . import Action
from .mixins import (
    TurboFrameResponseMixin,
    TurboFrameTemplateResponseMixin,
    TurboStreamAutoTargetMixin,
    TurboStreamFormMixin,
    TurboStreamResponseMixin,
    TurboStreamTemplateResponseMixin,
)


class TurboStreamView(TurboStreamResponseMixin, View):
    """Renders a simple turbo-stream view"""

    def dispatch(self, *args, **kwargs):
        return self.render_turbo_stream_response()


class TurboStreamTemplateView(TurboStreamTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-stream> tags. """

    def render_to_response(self, context, **response_kwargs):
        return self.render_turbo_stream_response(context, **response_kwargs)


class TurboStreamFormView(TurboStreamFormMixin, FormView):
    ...


class TurboStreamCreateView(
    TurboStreamAutoTargetMixin, TurboStreamFormMixin, CreateView
):
    turbo_stream_target_suffix = "-form"


class TurboStreamUpdateView(
    TurboStreamAutoTargetMixin, TurboStreamFormMixin, UpdateView
):
    turbo_stream_target_suffix = "-form"


class TurboStreamDeleteView(TurboStreamResponseMixin, DeleteView):
    """Handles a delete action, returning an empty turbo-stream "remove"
    response.
    """

    turbo_stream_action = Action.REMOVE

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.render_turbo_stream_response()


class TurboFrameView(TurboFrameResponseMixin, View):
    """Retuns a simple turbo-frame response."""

    def dispatch(self, *args, **kwargs):
        return self.render_turbo_frame_response()


class TurboFrameTemplateView(TurboFrameTemplateResponseMixin, TemplateView):
    """Renders response template inside <turbo-frame> tags. """

    def render_to_response(self, context, **response_kwargs):
        return self.render_turbo_frame_response(context, **response_kwargs)
