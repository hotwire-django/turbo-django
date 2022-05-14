from turbo.classes import Stream
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class BaseComponent(Stream):

    template_name = None

    def get_context(self):
        """
        Return the default context to render a component.
        """
        return {}

    def compute_context(self, context, **context_kwargs):
        """
        Calculate the context to render.
        """
        new_context = self.get_context()
        if context:
            new_context.update(context)
        new_context.update(context_kwargs)

        return new_context

    def render(self, context={}, **context_kwargs):
        context = self.compute_context(context, **context_kwargs)
        self.update(self.template_name, context, id=self.stream_name)

    def initial_render(self, context):
        """
        Returns the html origially rendered on the page.
        """
        context = self.compute_context(context)
        return render_to_string(self.template_name, context)


class BroadcastComponent(BaseComponent):
    """
    A component that broadcasts the same content to all subscribed users.
    """

    pass


class UserBroadcastComponent(BaseComponent):
    """
    A component that broadcasts a template to a specific user.
    """

    template_name = None

    def __init__(self, user):

        if user is None:
            user = AnonymousUser

        try:
            if not isinstance(user, get_user_model()):
                user = get_user_model().objects.get(pk=user)
        except TypeError:
            pass

        self.user = user
        super().__init__()

    def get_init_args(self):
        return [self.user.pk]

    def user_passes_test(self, request_user):
        if request_user and request_user.is_authenticated:
            return True
