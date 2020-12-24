from django.shortcuts import render
from django.http import HttpResponse

def render_turbo(request, template_name, location, context=None, content_type="text/html", status=None, using=None):
    # A request could be made from 2 places.

    # Either it is a Turbo Frame that initiated the request: we can detect it with
    # `turbo-stream` in the `Accept` header.
    if "turbo-stream" in request.META['HTTP_ACCEPT']:
        # Notify the template that this is a trubo stream response sent over HTTP
        # (in opposition to turbo steams sent via websockets)
        context["turbo__is_http"] = True

        # Notify the turbo client that we are sending a turbo-stream message
        # so the frontend does not try to redirect the user
        content_type = '%s; turbo-stream;' % content_type

        return render(request=request, template_name=template_name, context=context, content_type=content_type, status=status, using=using)

    # Otherwise, the request was made by a plain old webpage, without any JS
    # We return an HTTP 303 See Other like the Turbo documentation recommends
    # so the user is redirected somwhere they can see the result of their action
    else:
        response = HttpResponse(content="", status=303)
        response["Location"] = location
        return response
