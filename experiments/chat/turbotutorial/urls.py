"""turbotutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import TemplateView

from chat import views

urlpatterns = [
    path("", views.RoomList.as_view(), name="room_list"),
    path("<slug:pk>/", views.RoomDetail.as_view(), name="room_detail"),
    path("<slug:pk>/message_create", views.MessageCreate.as_view(), name="message_create"),
    path("message/<int:message_id>/delete", views.message_delete, name="message_delete"),
]
