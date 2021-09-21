from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from django.forms import ModelForm

from .models import Event

# Formclass. Can be used to both add new and to alter existing.
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'location', 'min_price', 'max_price', 'description']
        #fields = '__all__'


class DisplayEventsView(TemplateView):
    template_name = "happenings/events.html"

class MyEventsView(ListView):
    template_name = "happenings/my_events.html"
    context_object_name = "my_events_list"
    def get_queryset(self):
        return Event.objects.order_by('-name') 

class AddNewEvent(CreateView):
    template_name = "happenings/add_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('my_events')


