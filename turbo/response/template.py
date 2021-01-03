# Django
from django.template.loader import render_to_string

# Local
from .renderers import render_turbo_frame, render_turbo_stream


def render_turbo_stream_template(
    template, context, *, action, target, **template_kwargs
):
    """Renders a *<turbo-stream>* template.

    :param template: template name or names
    :param context: template context
    :param action: turbo-stream action
    :param target: turbo-stream target
    :type template: list or str
    :type context: dict
    :type action: turbo_response.Action
    :type target: str

    :rtype: str
    """
    return render_turbo_stream(
        action,
        target,
        render_to_string(
            template,
            {
                **context,
                "turbo_stream_target": target,
                "turbo_stream_action": action.value,
                "is_turbo_stream": True,
            },
            **template_kwargs,
        ),
    )


def render_turbo_frame_template(template, context, *, dom_id, **kwargs):
    """Renders a *<turbo-frame>* template.

    :param template: template name or names
    :param context: template context
    :param dom: turbo-frame DOM ID
    :type template: list or str
    :type context: dict
    :type dom_id: str

    :rtype: str
    """

    return render_turbo_frame(
        dom_id,
        render_to_string(
            template,
            {**context, "turbo_frame_dom_id": dom_id, "is_turbo_frame": True},
            **kwargs,
        ),
    )
