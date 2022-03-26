from .classes import TurboRender


def render_frame(request, template_name: str, context=None) -> "TurboRender":
    """
    Returns a TurboRender object from a django template.  This rendered template
    can then be broadcast to subscribers with the TurboRender actions
    (eg: append, update, etc...)

    Takes a template name and context identical to Django's render() method.
    """
    return TurboRender.init_from_template(template_name, context=context, request=request)


def render_frame_string(text: str) -> "TurboRender":
    """
    Returns a TurboRender object from a string.
    """

    return TurboRender(text)


def remove_frame(selector=None, id=None) -> "TurboRender":
    """
    Returns a removal frame.  These don't use a template.
    """

    return TurboRender().remove(selector, id)
