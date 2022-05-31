from datetime import datetime
from django.shortcuts import render
from turbo.shortcuts import render_frame, remove_frame

from .streams import *


def components_demo_view(request):

    return render(request, "app/home.html", {})
