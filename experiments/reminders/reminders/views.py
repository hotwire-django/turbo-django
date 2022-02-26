from datetime import datetime
from django.shortcuts import render
from turbo.shortcuts import render_frame, remove_frame

from .models import Reminder
from .forms import ReminderForm


def reminder_list(request):
    return render(request, "reminders/reminder_list.html", {"reminders": Reminder.objects.all()})


def reminder_list_form(request):

    if request.method == "POST":

        action = request.POST.get('action')

        if action == 'Delete All':
            Reminder.objects.all().delete()
            frame = remove_frame(selector='#reminders li')
            return frame.response

        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save()
            frame = render_frame(
                "reminders/reminder_list_item.html", {'reminder': reminder}
            ).append(id='reminders')
            return frame.response

    else:
        form = ReminderForm()

    return render(request, "reminders/reminder_list_form.html", {"form": form})


def reminder_list_search(request):
    # Post request to search
    reminders = Reminder.objects.filter(reminder_text__icontains=request.POST.get('search', ''))
    frame = render_frame("reminders/reminder_list_items.html", {"reminders": reminders})
    return frame.replace(id='reminders').response
