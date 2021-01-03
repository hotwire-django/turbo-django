from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

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


