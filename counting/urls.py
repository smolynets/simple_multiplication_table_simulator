from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("server_time/", views.server_time_view, name="server_time"),
]
