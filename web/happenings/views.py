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
