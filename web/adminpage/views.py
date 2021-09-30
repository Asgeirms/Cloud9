from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from happenings.models import Schedule


class CurateEventsView(ListView):
    template_name = "adminpage/cureate_events.html"
    model = Schedule
    context_object_name = "scheduled_events"
