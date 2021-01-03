# Django
from django.core.exceptions import ImproperlyConfigured
from django.db import models

# Local
from . import Action
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)

class TurboStreamResponseMixin:
    """Mixin to handle turbo-stream responses"""

    turbo_stream_action = None
    turbo_stream_target = None

    def get_turbo_stream_action(self):
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        :rtype: turbo_response.Action
        """
        return self.turbo_stream_action

    def get_turbo_stream_target(self):
        """Returns the turbo-stream target parameter

        :return: turbo-stream target
        :rtype: str
        """
        return self.turbo_stream_target

    def get_response_content(self):
        """Returns turbo-stream content.

        :rtype: str
        """

        return ""

    def render_turbo_stream_response(self, **response_kwargs):
        """Returns a turbo-stream response.

        :rtype: turbo_response.TurboStreamResponse
        """

        action = self.get_turbo_stream_action()
        target = self.get_turbo_stream_target()

        if action is None:
            raise ValueError("action must be specified")

        if target is None:
            raise ValueError("target must be specified")

        return TurboStreamResponse(
            action=action,
            target=target,
            content=self.get_response_content(),
            **response_kwargs,
        )


class TurboStreamTemplateResponseMixin(TurboStreamResponseMixin):
    """Handles turbo-stream template responses."""

    def get_turbo_stream_template_names(self):
        """Returns list of template names.

        :rtype: list
        """
        return self.get_template_names()

    def render_turbo_stream_response(self, context, **response_kwargs):
        """Renders a turbo-stream template response.

        :param context: template context
        :type context: dict

        :rtype: turbo_response.TurboStreamTemplateResponse
        """
        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=self.get_turbo_stream_target(),
            action=self.get_turbo_stream_action(),
            context=context,
            using=self.template_engine,
        )


class PartialTemplateResolverMixin(TurboStreamTemplateResponseMixin):
    """Handles automatic template name resolution for partial
    include templates. This is useful for views that may return a normal
    HttpResponse (e.g. a full-page HTML document or redirect) but
    may also return a turbo-stream, for example a form partial with
    validation errors.

    The class will automatically prepend an underscore to your template name.

    For example, if your main template is *myapp/my_form.html*, the turbo-stream
    response will look for the template *my_app/_my_form.html*.
    """

    partial_template_prefix = "_"
    turbo_stream_template_name = None

    def get_partial_template_names(self):
        def resolve_name(name):
            start, part, end = name.rpartition("/")
            return "".join([start, part, self.partial_template_prefix, end])

        return [resolve_name(name) for name in self.get_template_names()]

    def get_turbo_stream_template_names(self):
        """Returns list of template names. Names will be automatically
        prefixed with underscore. If you want to use a specific template name
        instead, just set the property **turbo_stream_template_name**.

        :rtype: list
        """

        return (
            [self.turbo_stream_template_name]
            if self.turbo_stream_template_name
            else self.get_partial_template_names()
        )


class TurboStreamAutoTargetMixin:
    """Generates the stream target DOM ID based on model metadata.

    If *self.object* is present the DOM ID will be:

    *<app-name>-<model-name>-<object_id>*

    otherwise:

    *<app-name>-<model-name>*

    You can override by explicitly setting **turbo_stream_target**.
    """

    turbo_stream_target_suffix = ""

    def get_turbo_stream_target(self):
        if self.turbo_stream_target is not None:
            return self.turbo_stream_target

        if hasattr(self, "object") and isinstance(self.object, models.Model):
            target = [
                self.object._meta.app_label,
                self.object._meta.model_name,
            ]
            if self.object.pk:
                target.append(str(self.object.pk))

            return "-".join(target) + self.turbo_stream_target_suffix

        elif hasattr(self, "model") and issubclass(self.model, models.Model):
            return (
                "-".join([self.model._meta.app_label, self.model._meta.model_name,])
                + self.turbo_stream_target_suffix
            )

        raise ImproperlyConfigured("No Django model instance found")


class TurboStreamFormMixin(PartialTemplateResolverMixin):
    """Mixin for handling form validation. If the form is
    invalid, returns a turbo-stream response instead."""

    turbo_stream_action = Action.REPLACE

    def form_invalid(self, form):
        return self.render_turbo_stream_response(self.get_context_data(form=form))

    def get_context_data(self, **context):
        """Adds the target to both templates, so we can keep them consistent"""
        self.turbo_stream_target = self.get_turbo_stream_target()

        return {
            **super().get_context_data(),
            "turbo_stream_target": self.turbo_stream_target,
        }


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self):
        return self.turbo_frame_dom_id

    def get_response_content(self):
        return ""

    def render_turbo_frame_response(self, **response_kwargs):

        dom_id = self.get_turbo_frame_dom_id()
        if dom_id is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameResponse(
            content=self.get_response_content(),
            dom_id=self.get_turbo_frame_dom_id(),
            **response_kwargs,
        )


class TurboFrameTemplateResponseMixin(TurboFrameResponseMixin):
    """Handles turbo-frame template responses."""

    def render_turbo_frame_response(self, context, **response_kwargs):
        """Returns a turbo-frame response.

        :param context: template context
        :type context: dict

        :rtype: turbo_response.TurboFrameTemplateResponse
        """
        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=self.get_turbo_frame_dom_id(),
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )
