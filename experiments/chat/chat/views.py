from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404
from chat.models import Room, Message


class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'


class RoomDetail(DetailView):
    model = Room
    context_object_name = 'room'


class MessageCreate(CreateView):
    model = Message
    fields = ["text"]

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        form.instance.room = room
        super().form_valid(form)
        return render(self.request, 'chat/message_update.html', {"message": form.instance}, content_type='text/html; turbo-stream;')


