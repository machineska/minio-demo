from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload, name="upload"),
    path("list", views.list_view, name="list"),
    path("presign/<path:key>", views.presign, name="presign"),
    path("delete/<path:key>", views.delete, name="delete"),
    path("versions/<path:key>", views.versions, name="versions"),
    path("restore/<path:key>/<path:version_id>", views.restore, name="restore"),
    path("events/webhook", views.events_webhook, name="events_webhook"),
    path("events", views.events_view, name="events_view"),
]
