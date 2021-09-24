from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.forms import ModelForm

from .models import Event, Schedule
from random import randint

# Formclass. Can be used to both add new and to alter existing objects.
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'min_price', 'max_price', 'description']
        #fields = '__all__'

# View you own events
class MyEventsView(ListView):
    template_name = "happenings/my_events.html"
    context_object_name = "my_events_list"
    # TODO: sort out only your events, not all.
    def get_queryset(self):
        return Event.objects.order_by('-name') 

class DetailedEventView(DetailView):
    model = Event
    template_name = 'happenings/event_detail.html'
    context_object_name = "event"

class AddNewEvent(CreateView):
    template_name = "happenings/add_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('my_events')
#---------------------------------------------------------------
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

