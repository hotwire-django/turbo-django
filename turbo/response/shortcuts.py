# Local
from .renderers import Action, render_turbo_frame, render_turbo_stream
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)
from .template import render_turbo_frame_template, render_turbo_stream_template


class TurboStream:
    """Class for creating Turbo Stream strings and responses."""

    def __init__(self, target):
        """
        :param target: stream target
        :type target: str
        """
        self.target = target

    @property
    def append(self):
        """
        :rtype: TurboStreamAction
        """
        return TurboStreamAction(self.target, Action.APPEND)

    @property
    def prepend(self):
        """
        :rtype: TurboStreamAction
        """
        return TurboStreamAction(self.target, Action.PREPEND)

    @property
    def remove(self):
        """
        :rtype: TurboStreamAction
        """
        return TurboStreamAction(self.target, Action.REMOVE)

    @property
    def replace(self):
        """
        :rtype: TurboStreamAction
        """
        return TurboStreamAction(self.target, Action.REPLACE)

    @property
    def update(self):
        """
        :rtype: TurboStreamAction
        """
        return TurboStreamAction(self.target, Action.UPDATE)


class TurboStreamAction:
    """Returns strings and responses for a specific Turbo Stream action type."""

    def __init__(self, target, action):
        """
        :param target: Turbo Stream target
        :param action: Turbo Stream action
        :type target: str
        :type action: str
        """
        self.action = action
        self.target = target

    def render(self, content=""):
        """
        :param content: enclosed content
        :type content: str

        :return: a *<turbo-stream>* string
        :rtype: str
        """
        return render_turbo_stream(
            action=self.action, target=self.target, content=content
        )

    def response(self, content="", **response_kwargs):
        """
        :param content: enclosed content
        :type content: str

        :return: a *<turbo-stream>* HTTP response
        :rtype: turbo_response.TurboStreamResponse
        """
        return TurboStreamResponse(
            action=self.action, target=self.target, content=content, **response_kwargs
        )

    def template(self, template_name, context=None, **template_kwargs):
        """
        :param template_name: Django template name
        :param context: template context

        :type template_name: str or list
        :type context: dict

        :return: a *<turbo-stream>* HTTP response
        :rtype: TurboStreamTemplateProxy
        """
        return TurboStreamTemplateProxy(
            template_name,
            context,
            action=self.action,
            target=self.target,
            **template_kwargs
        )


class TurboStreamTemplateProxy:
    """Wraps template functionality."""

    def __init__(self, template_name, context, *, action, target, **template_kwargs):
        self.action = action
        self.target = target
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs

    def render(self):
        """
        :return: rendered template string
        :rtype: str
        """
        return render_turbo_stream_template(
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **self.template_kwargs
        )

    def response(self, request, **kwargs):
        """
        :return: HTTP response
        :rtype: turbo_response.TurboStreamTemplateResponse
        """
        return TurboStreamTemplateResponse(
            request,
            self.template_name,
            self.context,
            action=self.action,
            target=self.target,
            **{**self.template_kwargs, **kwargs}
        )


class TurboFrame:
    """Class for creating Turbo Frame strings and responses."""

    def __init__(self, dom_id):
        """
        :param dom_id: DOM ID of turbo frame
        :type dom_id: str
        """
        self.dom_id = dom_id

    def render(self, content=""):
        """
        :param content: enclosed content
        :type content: str

        :return: a *<turbo-frame>* string
        :rtype: str
        """
        return render_turbo_frame(dom_id=self.dom_id, content=content)

    def response(self, content="", **response_kwargs):
        """
        :param content: enclosed content
        :type content: str

        :return: a *<turbo-frame>* HTTP response
        :rtype: turbo_response.TurboFrameResponse
        """
        return TurboFrameResponse(
            dom_id=self.dom_id, content=content, **response_kwargs
        )

    def template(self, template_name, context=None, **template_kwargs):
        """
        :param template_name: Django template name
        :param context: template context

        :type template_name: str or list
        :type context: dict

        :return: a *<turbo-frame>* HTTP response
        :rtype: TurboFrameTemplateProxy
        """
        return TurboFrameTemplateProxy(
            template_name, context, dom_id=self.dom_id, **template_kwargs
        )


class TurboFrameTemplateProxy:
    """Wraps template functionality."""

    def __init__(self, template_name, context, *, dom_id, **template_kwargs):
        self.template_name = template_name
        self.context = context
        self.template_kwargs = template_kwargs
        self.dom_id = dom_id

    def render(self):
        """
        :param content: enclosed content
        :type content: str

        :return: a *<turbo-frame>* string
        :rtype: str
        """
        return render_turbo_frame_template(
            self.template_name, self.context, dom_id=self.dom_id, **self.template_kwargs
        )

    def response(self, request, **kwargs):
        """
        :return: HTTP response
        :rtype: turbo_response.TurboFrameTemplateResponse
        """
        return TurboFrameTemplateResponse(
            request,
            self.template_name,
            self.context,
            dom_id=self.dom_id,
            **{**self.template_kwargs, **kwargs}
        )
