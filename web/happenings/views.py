from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy

from .forms import EventForm

from .models import Event, Schedule
from random import randint
from datetime import datetime


class MyEventsView(ListView):
    '''View you own events'''
    template_name = "happenings/my_events_list_view.html"
    context_object_name = "my_events_list"
    
    # TODO: sort out only your events, not all.
    def get_queryset(self):
        return Event.objects.order_by('-name') 

class DetailedMyEventView(DetailView):
    '''The detailed view you get watching your own events.'''
    model = Schedule
    template_name = 'happenings/my_event_detail_view.html'
    context_object_name = 'scheduled_event'
    success_url = reverse_lazy('my_events')
    
class SuggestEventView(CreateView):
    template_name = "happenings/suggest_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('my_events')


class EventListView(ListView):
    model = Schedule
    queryset = Schedule.objects.filter(event__admin_approved=True).filter(end_time__gte=datetime.now()).order_by('start_time')
    template_name = "happenings/event_list_view.html"
    context_object_name = "scheduled_events_list"


class EventView(DetailView):
    model = Schedule
    template_name = "happenings/event_detail_view.html"
    context_object_name = 'scheduled_event'
    success_url = reverse_lazy('events')


class RandomEventView(DetailView):
    queryset = Schedule.objects.all()
    template_name = "happenings/event_detail_view.html"
    context_object_name = 'scheduled_event'

    def get_object(self):
        object_list = Schedule.objects.filter(event__admin_approved=True).filter(end_time__gte=datetime.now())
        if (len(object_list) > 1):
            number = randint(0, len(object_list)-1)
            return object_list[number]
        return None

