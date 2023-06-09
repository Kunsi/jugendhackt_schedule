from django.contrib import admin

from .models import Event, Language, License, Person, Room, ScheduleEntry


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "acronym", "start", "last_day"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "event", "has_recording"]


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = ["title", "start", "room", "full_slug"]
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["name", "short"]


admin.site.register(License)
