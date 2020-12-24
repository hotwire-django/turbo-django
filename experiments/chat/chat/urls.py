from django.urls import path

from . import views

urlpatterns = [
    path("", views.RoomList.as_view(), name="index"),
    path("<slug:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<slug:pk>/send", views.MessageCreate.as_view(), name="send"),
]
