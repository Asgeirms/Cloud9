from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import EventForm, ScheduleForm, EditEventForm

from .models import Event, Schedule
from random import randint


class MyEventsListView(ListView):
    '''View you own events'''
    template_name = "happenings/my_events_list_view.html"
    context_object_name = "my_events_list"
    model = Event

    def get_queryset(self):
        # Only see your own events.
        return Event.objects.filter(host=self.request.user)


class DetailedMyScheduleView(DetailView):
    '''The detailed view you get watching your own events.'''
    model = Schedule
    template_name = 'happenings/my_schedules_detail_view.html'
    context_object_name = 'scheduled_event'
    success_url = reverse_lazy('my_events_detailed')


class DetailedMyEventView(DetailView):
    '''The detailed view you get watching your own events.'''
    model = Event
    template_name = 'happenings/my_event_detail_view.html'
    context_object_name = 'event'
    success_url = reverse_lazy('my_events')


class SuggestEventView(CreateView):
    template_name = "happenings/suggest_event.html"
    models = Event
    form_class = EventForm
    context_object_name = "event"
    success_url = reverse_lazy('my_events')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['schedule_form'] = ScheduleForm(self.request.POST)
        else:
            context['schedule_form'] = ScheduleForm()
        
        return context

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        
        form.instance.host = self.request.user
        
        # Attaching a schedule form with its fields 
        schedule_form = context['schedule_form']
        if schedule_form.is_valid():
            # Very dirty hack
            self.object = form.save()
            schedule_form.instance.event = self.object
            schedule_form.save()

            # Super(). allows you to alter the django super-class, without breaking it.
            return super().form_valid(form)
        else:

            # If not successful, keep the existent data on form 
            return self.render_to_response(self.get_context_data(form=form))


class EditEventView(UpdateView):
    template_name = "happenings/update_event.html"
    model = Event
    form_class = EditEventForm
    context_object_name = "event"

    def get_success_url(self):
        event_id = self.kwargs['pk']
        return reverse_lazy('my_events_detailed', kwargs={'pk': event_id})


class DeleteEventView(DeleteView):
    model = Event
    success_url = reverse_lazy('my_events')


class AddScheduleView(CreateView):
    template_name = "happenings/add_schedule.html"
    model = Schedule
    form_class = ScheduleForm
    context_object_name = "schedule"

    def form_valid(self, form, **kwargs):
        form.instance.event_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        event_id = self.kwargs['pk']
        return reverse_lazy('my_events_detailed', kwargs={'pk': event_id})


class EditScheduleView(UpdateView):
    template_name = "happenings/update_schedule.html"
    model = Schedule
    form_class = ScheduleForm
    context_object_name = "scheduled_event"

    def get_success_url(self):
        schedule_id = self.kwargs['pk']
        return reverse_lazy('my_schedule_detailed', kwargs={'pk': schedule_id})


class DeleteScheduleView(DeleteView):
    model = Schedule

    def get_success_url(self):
        event_id = self.kwargs['pk']
        return reverse_lazy('my_events_detailed', kwargs={'pk': event_id})


class EventListView(ListView):
    model = Schedule
    queryset = Schedule.objects.filter(event__admin_approved=True).filter(end_time__gte=timezone.now()).order_by('start_time')
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
        object_list = Schedule.objects.filter(event__admin_approved=True).filter(end_time__gte=timezone.now())
        if len(object_list) > 0:
            number = randint(0, len(object_list)-1)
            return object_list[number]
        return None


class SwipeFinishView(TemplateView):
    template_name = "happenings/swipe_finish.html"
