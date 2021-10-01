from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.forms import ModelForm, TextInput

from .models import Event, Schedule
from random import randint
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect

class EventForm(ModelForm):
    '''Formclass. Can be used to both add new and to alter existing.'''
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

class MyEventsListView(ListView):
    '''View you own events'''
    template_name = "happenings/my_events_list_view.html"
    context_object_name = "my_events_list"
    model = Schedule
    def get_queryset(self):
        return Schedule.objects.filter(event__host=self.request.user)


class DetailedMyEventView(DetailView):
    '''The detailed view you get watching your own events.'''
    model = Schedule
    template_name = 'happenings/my_event_detail_view.html'
    context_object_name = 'scheduled_event'
    success_url = reverse_lazy('my_events')


class AddEventView(CreateView):
    template_name = "happenings/add_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('my_events')
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.host = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


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
        if len(object_list) > 0:
            number = randint(0, len(object_list)-1)
            return object_list[number]
        return None

