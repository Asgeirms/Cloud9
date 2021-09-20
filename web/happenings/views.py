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

