from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from turbo import APPEND
from turbo.mixins import BroadcastableMixin
from .models import Room, Message


class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'


class RoomDetail(DetailView):
    model = Room
    context_object_name = 'room'


class RoomUpdate(UpdateView):
    model = Room
    fields = ["name"]


class MessageCreate(CreateView):
    model = Message
    fields = ["text"]

    def get_success_url(self):
        # Redirect to the empty form
        return reverse("send", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        form.instance.room = room
        return super().form_valid(form)


def wiretap(request):
    """
    This is a View that just receives all messages sent in all rooms while its connected.
    """
    return render(request, 'chat/wiretap.html', {})


class TriggerBroadcast(BroadcastableMixin, View):
    """
    Example View that just triggers a Broadcast Message to all Channels
    WITHOUT Storing it actually as Message, so not using the BroadcastabelModelMixin.
    """

    def get_turbo_streams_template(self, target):
        return 'chat/message.html'

    def append_context(self, target):
        return {"message": Message(text="This is a broadcast that will not be stored as Message!")}

    def get_dom_target(self, target):
        return f'messages'

    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            self.send_broadcast(room, action=APPEND)
        return HttpResponse('Sent a Broadcast')


