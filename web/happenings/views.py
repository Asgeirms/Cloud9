from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Event

# Create your views here.
class DisplayEventsView(TemplateView):
    template_name = "happenings/events.html"

class AddNewEvent(CreateView):
    template_name = "happenings/add_event.html"
    models = Event
    fields = '__all__'
    context_object_name = "event"
    success_url = reverse_lazy('all-events')

    def get_queryset(self):
        return Event.objects.all()

