from django import shortcuts
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Case, When # to order querysets on list of ids

from .forms import EventForm, ScheduleForm, FilterForm, EditEventForm

from .models import Event, Schedule
from random import randint


class MyEventsListView(ListView):
    '''View you own events'''
    template_name = "happenings/my_events_list_view.html"

    context_object_name = "my_events_list"
    model = Event

    def get_queryset(self):
        '''The task of this query:
            - Users should only see their own events.
            - Find what schedule belonging to what event, and sort events on schedules.
        '''
        current_schedules = Schedule.objects.filter(event__host=self.request.user).filter(end_time__gte=timezone.now()).order_by('start_time')
        old_schedules = Schedule.objects.filter(event__host=self.request.user).filter(end_time__lt=timezone.now()).order_by('start_time')

        current_pks = []
        old_pks = []
        for schedule in current_schedules:
            if schedule.event.id not in current_pks:
                current_pks.append(schedule.event.id)
        
        for schedule in old_schedules:
            if schedule.event.id not in old_pks and schedule.event.id not in current_pks:
                old_pks.append(schedule.event.id)

        # Now current_pks contains all event_id's ordered
        preserved_current = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(current_pks)])
        preserved_old = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(old_pks)])

        queryset = {'current' : Event.objects.filter(pk__in=current_pks).order_by(preserved_current),
                    'expired' : Event.objects.filter(pk__in=old_pks).order_by(preserved_old),
                    }

        # My own swipes as query
        queryset['my_swipes'] = self.request.user.interested_events.all()
        return queryset


class DetailedMyScheduleView(DetailView):
    '''The detailed view you get watching your own event-schedules.'''
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

def FilterEventListView(request):
    queryset = Schedule.objects.all()
    queryset = queryset.filter(event__admin_approved=True)
    queryset = queryset.order_by('start_time')
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            max_price = form.cleaned_data.get("max_price")
            from_time = form.cleaned_data.get("from_time")
            to_time = form.cleaned_data.get("to_time")
            if max_price:
                queryset = queryset.filter(event__min_price__lte=max_price)
            if from_time:
                queryset = queryset.filter(end_time__gte=from_time)
            if to_time:
                queryset = queryset.filter(start_time__lte=to_time)
    else:
        form = FilterForm({'from_time': timezone.now()})
        queryset = queryset.filter(end_time__gte=timezone.now())
    return render(request, 'happenings/filter.html', {'form': form, 'queryset': queryset})

