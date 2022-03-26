=============
Turbo Frames
=============

.. module:: turbo.Turbo

Turbo Frames can be rendered in python using convience methods.

.. module:: turbo.shortcuts

.. method:: render_frame(request, template_name: str, context=None) -> TurboRender

.. method:: render_frame_string(text: str) -> TurboRender

.. method:: remove_frame(selector=None, id=None) -> TurboRender

    Create a TurboRender object that removes a frame.  Since there is no content to be inserted, no template or text is passed.  Instead,

.. code-block:: python

    from turbo.shortcuts import render_frame, remove_frame

    def post(self, request, *args, **kwargs):

        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()

            new_form = RoomForm()

            return (
                render_frame(
                    request,
                    "chat/components/create_room_form.html",
                    {"form": new_form},
                )
                .replace(id="create-room-form")
                .response
            )



TurboRender methods
===================

.. module:: turbo.TurboRender

Once a turbo frame has been rendered, it needs to know where to position itself.  The following methods let the client page know where to position the new content when it is received.

The typical use is to chain ``render`` and ``.<action>`` commands into one logical, easy-to-read statement.

.. code-block:: python

    render_frame(
        request, 'broadcast.html', {'content': "New message!"}
    ).update(".alert_box")

Each of the following methods take either an ``selector`` or ``id`` keyword argument to specify which HTML element will receive the action.  ``selector``is the first argument, so no keyword specifier is needed.


.. method:: append(selector=None, id=None)

    Add the rendered template to the end of the specified HTML element.

.. method:: prepend(selector=None, id=None)

    Add the rendered template to the beginning of the specified HTML element.

.. method:: replace(selector=None, id=None)

    Remove and replace the specified HTML element with the rendered template.

.. method:: update(selector=None, id=None)

    Replace the contents inside the specified HTML element with the rendered template.

.. method:: remove(selector=None, id=None)

    Remove the given HTML element.  The rendered template will not be used.  As no template is used to remove divs, this can also be called directly from the shortcut ``remove_frame()``.  Ex: ``remove_frame(id='div_to_remove')``

.. method:: before(selector=None, id=None)

    Insert the rendered template before the specified HTML element.

.. method:: after(selector=None, id=None)

    Insert the template after the specified HTML element.

.. method:: response

    Property.  Return this rendered template as an HttpResponse with a "text/vnd.turbo-stream.html" content type.  This allows for turbo-stream elements to be returned from a form submission.  See the Turbo documentation for more detail (https://turbo.hotwired.dev/handbook/drive#streaming-after-a-form-submission)

    .. code-block:: python

        frame = render_frame(
                request, "reminders/reminder_list_item.html", {'reminder': reminder}
        ).append(id='reminders')
        return frame.response

