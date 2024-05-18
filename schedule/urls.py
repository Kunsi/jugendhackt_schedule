from django.urls import path

from . import views

urlpatterns = [
    path("schedule/<slug:slug>.json", views.schedule_json, name="schedule_json"),
    path("schedule/<slug:slug>.xml", views.schedule_xml, name="schedule_xml"),
    path("schedule/<slug:slug>.html", views.schedule_html, name="schedule_html"),
    path("", views.index, name="index"),
]
