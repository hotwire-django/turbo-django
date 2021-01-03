# Standard Library
import enum


class Action(enum.Enum):
    """Turbo-Stream action parameter"""

    APPEND = "append"
    PREPEND = "prepend"
    REMOVE = "remove"
    REPLACE = "replace"
    UPDATE = "update"


def render_turbo_stream(action, target, content=""):
    """Wraps content in correct <turbo-stream> tags.

    :param action: action type
    :param target: the DOM ID target of the stream
    :param content: content to be wrapped. Can be empty.

    :type action: turbo_response.Action
    :type target: str
    :type content: str

    :return: *<turbo-stream>* string
    :rtype: str

    """
    return f'<turbo-stream action="{action.value}" target="{target}"><template>{content.strip()}</template></turbo-stream>'


def render_turbo_frame(dom_id, content=""):
    """

    Wraps a response in correct *<turbo-frame>* tags.

    :param dom_id: a DOM ID present in the content
    :param content: content of the turbo-frame
    :type dom_id: str
    :type content: str

    :rtype: str
    """
    return f'<turbo-frame id="{dom_id}">{content.strip()}</turbo-frame>'
