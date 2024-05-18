from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Event, Room, ScheduleEntry



def index(request):
    today = datetime.now().replace(hour=0, minute=0, second=0)

    return render(
        request,
        "schedule/index.html",
        context={
            "events": Event.objects.all(),
        },
    )


def schedule_html(request, slug):
    event = get_object_or_404(Event, acronym=slug)

    schedule = {}
    for day in range(0, event.duration_days):
        schedule[day] = {
            "day": day + 1,
            "start": event.start + timedelta(days=day),
            "end": event.start + timedelta(days=day + 1),
            "events": ScheduleEntry.objects.filter(
                start__date=event.start + timedelta(days=day)
            ).order_by("start"),
        }

    return render(
        request,
        "schedule/schedule.html",
        context={
            "event": event,
            "schedule": schedule,
        },
    )


def schedule_xml(request, slug):
    event = get_object_or_404(Event, acronym=slug)

    schedule = {}

    for day in range(0, event.duration_days):
        schedule[day] = {
            "day": day + 1,
            "start": event.start + timedelta(days=day),
            "end": event.start + timedelta(days=day + 1),
            "rooms": {},
        }

        for room in Room.objects.filter(event=event):
            entries = ScheduleEntry.objects.filter(
                room=room, start__date=event.start + timedelta(days=day)
            ).order_by("start")
            if entries.count():
                schedule[day]["rooms"][room] = {
                    "name": room.name,
                    "uuid": room.uuid,
                    "events": entries,
                }

    return render(
        request,
        "schedule/schedule.xml",
        context={
            "event": event,
            "schedule": schedule,
        },
        content_type="application/xml",
    )


def schedule_json(request, slug):
    event = get_object_or_404(Event, acronym=slug)

    schedule = {
        "version": None,
        "conference": {
            "acronym": event.acronym,
            "title": event.name,
            "start": event.start.strftime("%Y-%m-%d"),
            "end": (event.start + timedelta(days=event.duration_days+1)).strftime("%Y-%m-%d"),
            "daysCount": event.duration_days,
            "timeslot_duration": "00:05",
            "rooms": [
                {
                    "name": room.name,
                    "guid": room.uuid,
                }
                for room in Room.objects.filter(event=event)
            ],
            "tracks": [],
            "days": [],
        },
    }

    for day in range(0, event.duration_days):
        day_schedule = {
            "index": day,
            "date": (event.start + timedelta(days=day)).strftime("%Y-%m-%d"),
            "day_start": (event.start + timedelta(days=day)).isoformat(),
            "day_end": (event.start + timedelta(days=day+1)).isoformat(),
            "rooms": {},
        }

        for room in Room.objects.filter(event=event):
            day_schedule["rooms"][room.name] = []
            for entry in  ScheduleEntry.objects.filter(
                room=room, start__date=event.start + timedelta(days=day)
            ).order_by("start"):
                day_schedule["rooms"][room.name].append({
                    "id": entry.pk,
                    "guid": entry.uuid,
                    "date": entry.start.isoformat(),
                    "start": entry.start.strftime("%H:%M"),
                    "logo": None,
                    "duration": entry.duration_hhmm,
                    "room": room.name,
                    "slug": entry.full_slug,
                    "title": entry.title,
                    "subtitle": "",
                    "track": None,
                    "type": "unknown",
                    "abstract": entry.abstract,
                    "description": None,
                    "recording_license": "",
                    "do_not_record": entry.recording_optout,
                    "persons": [
                        {
                            "public_name": person.name,
                        } for person in entry.persons.all()
                    ],
                    "links": [],
                    "attachments": [],
                })
        schedule["conference"]["days"].append(day_schedule)

    return JsonResponse(schedule)
