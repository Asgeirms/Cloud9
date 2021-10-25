import json
from datetime import datetime

from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.utils import timezone

from happenings.models import Schedule
from swiping.paginator import SwipingPaginator
from util.session_utils import add_data_to_session_as_dict, read_session_data
from happenings.views import use_session_filter, fill_filter_form_from_session, save_filters_to_session, reset_session_filters
from happenings.forms import FilterForm

class SwipingEventsView(ListView):
    template_name = "swiping/swiping.html"
    paginate_by = 1
    paginator_class = SwipingPaginator  
    model = Schedule

    viewed_events_name = "viewed_events"
    anon_yes_name = "anon_yes"
    anon_no_name = "anon_no"

    def get(self, request, *args, **kwargs):
        events_seen = read_session_data(request, self.viewed_events_name)
        anon_yes = read_session_data(request, self.anon_yes_name)
        anon_no = read_session_data(request, self.anon_no_name)

        pages = self.get_queryset()
        swiped = request.GET.get('swiped')

        if pages.count() <= 1:
            return redirect('swiping_finish')
        
        # This is not beautiful
        # Attemps to find the current page based on if it was a refresh, swipe or swipe then refresh
        current_pk = request.GET.get('current', None)
        current_page = None
        
        if current_pk is None:
            current_page = pages.first()
            current_pk = current_page.pk  
        else:
            current_page = Schedule.objects.get(pk=current_pk)


        if swiped == "yes":
            add_data_to_session_as_dict(
                request=request,
                name=self.viewed_events_name,
                session=events_seen,
                key=current_pk,
                value=current_page
            )

            if self.request.user.is_anonymous:
                add_data_to_session_as_dict(
                    request=request,
                    name=self.anon_yes_name,
                    session=anon_yes,
                    key=current_pk,
                    value=current_page
                )
            else:

                # TODO: add to registred user for persistent data
                pass

        elif swiped == "no":
            add_data_to_session_as_dict(
                request=request,
                name=self.viewed_events_name,
                session=events_seen,
                key=current_pk,
                value=current_page
            )

            if self.request.user.is_anonymous:
                add_data_to_session_as_dict(
                    request=request,
                    name=self.anon_no_name,
                    session=anon_no,
                    key=current_pk,
                    value=current_page
                )
            else:

                # TODO: add to registred user for persistent data
                pass
           
        return super().get(request, *args, **kwargs)
    
    def post(self, *args, **kwargs):
        form = FilterForm(self.request.POST)
        #if apply filter button
        if 'submit' in (self.request.POST):
            if form.is_valid(): 
                save_filters_to_session(self.request, form)
        #if reset filter button
        if 'reset' in (self.request.POST):
            reset_session_filters(self.request)
            #resets the form
            form = FilterForm({'from_time': timezone.now()})
        context = self.get_context_data(object_list=self.get_queryset(), **kwargs)
        context["form"]=form
        context["is_empty"] = len(self.get_queryset()) == 0
        return render(self.request, "swiping/swiping.html", context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.session.get('filter')):
            form = fill_filter_form_from_session(self.request)
        else: 
            form = FilterForm({'from_time': timezone.now()})
        context["form"]=form
        return context

    def get_queryset(self):
        events_seen = read_session_data(self.request, self.viewed_events_name)
        queryset = Schedule.objects \
                    .filter(event__admin_approved=True)
        if self.request.session.get('filter'):
            queryset = use_session_filter(queryset, self.request)
        else:
            queryset = queryset.filter(end_time__gte=timezone.now())

        # Temporary solution to random order queryset using order_by('?')

        # Filtering seen events
        if events_seen:
            for pk in events_seen:
                queryset = queryset.exclude(pk=pk)

        # Anon user with multiple events
        if self.request.user.is_anonymous and events_seen:
            return queryset.order_by('?')

        # Registred user 
        elif self.request.user.is_authenticated:
            return queryset.order_by('?')
        

        return queryset.order_by('?')
    
class FinishSwipingView(TemplateView):
    template_name = "swiping/swipe_finish.html"
