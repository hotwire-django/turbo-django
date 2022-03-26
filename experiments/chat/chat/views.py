from datetime import datetime

from django.shortcuts import reverse, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView

from chat.models import Room, Message
from chat.streams import RoomListStream
from chat.forms import RoomForm

from turbo.shortcuts import render_frame, remove_frame


class RoomList(ListView):
    model = Room
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RoomForm()
        return context

    def post(self, request, *args, **kwargs):

        action = request.POST.get('action')
        if action == "Delete All":
            Room.objects.all().delete()
            RoomListStream().delete_all()
            return HttpResponse()

        form = RoomForm(request.POST)
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


class RoomDetail(DetailView):
    model = Room
    context_object_name = "room"


class MessageCreate(CreateView):
    model = Message
    fields = ["text"]
    template_name = "chat/components/send_message_form.html"

    def get_success_url(self):
        # Redirect to the empty form
        return reverse("message_create", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        form.instance.room = room
        return super().form_valid(form)


def message_delete(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    message.delete()
    return HttpResponse()
