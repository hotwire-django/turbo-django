from django.urls import path

from . import views

urlpatterns = [
    path("", views.RoomList.as_view(), name="index"),
    path("<slug:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<slug:pk>/edit", views.RoomUpdate.as_view(), name="update"),
    path("<slug:pk>/send", views.MessageCreate.as_view(), name="send"),
    path("wiretap", views.wiretap, name="wiretap"),
    path("broadcast", views.TriggerBroadcast.as_view(), name="broadcast"),
]
