from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from turbo.shortcuts import render_turbo
from .models import Room, Message
from .forms import MessageForm



class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'


class RoomDetail(DetailView):
    model = Room
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MessageForm()
        return context



class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm


    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        room = get_object_or_404(Room, pk=self.kwargs["pk"])
        form.instance.room = room
        super().form_valid(form)
        return render_turbo(self.request, 'chat/message_update.html', location=self.get_success_url(), context={"message": form.instance})
