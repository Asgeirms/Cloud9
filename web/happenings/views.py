from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from django.forms import ModelForm, TextInput, ValidationError

from .models import Event


# Formclass. Can be used to both add new and to alter existing.
class EventForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ['name', 'location', 'min_price', 'max_price', 'description']
        labels = {
            'min_price': 'Minimum price',
            'max_price': 'Maximum price'
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Your name'}),
            'location': TextInput(attrs={'placeholder': 'Where to host?'}),
        }


class DisplayEventsView(TemplateView):
    template_name = "happenings/events.html"

    
class AddEventView(CreateView):
    template_name = "happenings/add_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('all_events')
from random import randint, random
from django.views.generic import DetailView, ListView
from .models import Schedule


class EventList(ListView):
    model = Schedule
    queryset = Schedule.objects.filter(event__admin_approved=True)
    template_name = "event_list_view.html"
    context_object_name = "scheduled_events_list"


class EventView(DetailView):
    model = Schedule
    template_name = "event_detail_view.html"
    context_object_name = 'scheduled_event'


class RandomEventView(DetailView):
    queryset = Schedule.objects.all()
    template_name = "event_detail_view.html"
    context_object_name = 'scheduled_event'

    def get_object(self):
        object_list = Schedule.objects.filter(event__admin_approved=True)
        if (len(object_list) > 1):
            number = randint(0, len(object_list)-1)
            return object_list[number]
        return None

