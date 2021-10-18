from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from datetime import datetime

from .forms import EventForm, ScheduleForm, FilterForm, EditEventForm
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
        object_list = Schedule.objects.filter(event__admin_approved=True)
        if self.request.session.get("filter"):
            object_list = useSessionFilter(object_list, self.request)
        else:
            object_list = object_list.filter(end_time__gte=timezone.now())
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
        #if apply filter button
        if 'submit' in (request.POST):
            if form.is_valid(): 
                saveFiltersToSession(queryset, request, form)
                #Actual filtering of search
                queryset = useSessionFilter(queryset, request)
        #if reset filter button
        if 'reset' in (request.POST):
            resetSessionFilters()
            #resets the form
            form = FilterForm({'from_time': timezone.now()})
            queryset = queryset.filter(end_time__gte=timezone.now())
    else:
        if (request.session.get('filter')):
            form = FilterForm({'from_time': request.session.get('filter_from_time'),
            'to_time': request.session.get('filter_to_time'),
            'max_price': request.session.get('filter_max_price')})
            queryset = useSessionFilter(queryset, request)
        else: 
            form = FilterForm({'from_time': timezone.now()})
            queryset = queryset.filter(end_time__gte=timezone.now())
    return render(request, 'happenings/filtered_event_list_view.html', {'form': form, 'queryset': queryset})

def saveFiltersToSession(queryset, request, form):
    #Gets data from form
    max_price = form.cleaned_data.get("max_price")
    from_time = form.cleaned_data.get("from_time")
    to_time = form.cleaned_data.get("to_time")
    #Stores the filter to session
    #Used for check if filter should be applied
    request.session['filter'] = True
    request.session['filter_max_price'] = max_price
    #Converts datetime to string so it can be stored in JSON format
    if from_time:
        request.session['filter_from_time'] = from_time.strftime("%Y-%m-%d %H:%M")
    else:
        request.session['filter_from_time'] = None
    if to_time:
        request.session['filter_to_time'] = to_time.strftime("%Y-%m-%d %H:%M")
    else:
        request.session['filter_to_time'] = None
    return queryset

def resetSessionFilters(request):
    request.session['filter'] = False
    request.session['filter_max_price'] = None
    request.session['filter_from_time'] = None
    request.session['filter_to_time'] = None


#Uses the filtervalues stored in session in the request to filter events
def useSessionFilter(queryset, request):
    if (request.session.get('filter')):
        if request.session.get('filter_max_price') != None:
            queryset = queryset.filter(event__min_price__lte=request.session.get('filter_max_price'))
        if request.session.get('filter_from_time'):
            queryset = queryset.filter(end_time__gte=datetime.strptime(request.session.get('filter_from_time'), "%Y-%m-%d %H:%M"))
        if request.session.get('filter_to_time'):
            queryset = queryset.filter(start_time__lte=datetime.strptime(request.session.get('filter_to_time'), "%Y-%m-%d %H:%M"))
    return queryset
