from random import randint
from django.views.generic import DetailView, ListView
from .models import Schedule


class EventList(ListView):
    model = Schedule
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
        object_list = Schedule.objects.all()
        number = randint(1, len(object_list))
        return Schedule.objects.get(pk=number)

