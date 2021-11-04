import json
import time
from datetime import datetime

import numpy as np
from django.db.models import When, Case

from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.utils import timezone

from happenings.models import Schedule, InterestCategory, CategoryWeightsUser
from swiping.paginator import SwipingPaginator
from util.session_utils import add_data_to_session_as_dict, read_session_data
from happenings.views import use_session_filter, fill_filter_form_from_session, save_filters_to_session, reset_session_filters
from happenings.forms import FilterForm


DECREASE_RATE = 0.8


class SwipingEventsView(ListView):
    template_name = "swiping/swiping.html"
    paginate_by = 1
    paginator_class = SwipingPaginator  
    model = Schedule

    viewed_events_name = "viewed_events"
    anon_yes_name = "anon_yes"
    anon_no_name = "anon_no"

    def get(self, request, *args, **kwargs):
        ###############################
        # AI 1
        # Initialize all unseen weighted category for user.
        if not self.request.user.is_anonymous:
            for obj in InterestCategory.objects.all():
                if not len(CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=obj)):
                    CategoryWeightsUser.objects.create(user=self.request.user, category=obj, weight=1)
        ###############################

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
            ''' TODO Use AJAX to prevent page from refreshing 
            while still updating the HTML to get new events post 
            spinning animation, for yes and no swipes. Do 
            use time.sleep in the future'''
            time.sleep(4)
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
                # Add the event to the users "interesting events" 
                # --> can be done from both sides
                self.request.user.interested_events.add(
                    Schedule.objects.get(pk=current_page.id))
                ###############################
                # AI 2
                # Increase weights of categories belonging to this event.
                for cat in Schedule.objects.filter(pk=current_pk).first().event.interest_categories.all():
                    weight : float = CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=cat).first().weight
                    weight += (1-weight)*(DECREASE_RATE)
                    CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=cat).update(weight=weight)
                ###############################

        elif swiped == "no":
            ''' TODO Use AJAX to prevent page from refreshing 
            while still updating the HTML to get new events post 
            spinning animation, for yes and no swipes. Do
            not use time.sleep in the future.'''
            time.sleep(4)
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
                ###############################
                # AI 3
                # Decrease weights of categories belonging to this event.
                for cat in Schedule.objects.filter(pk=current_pk).first().event.interest_categories.all():
                    weight = CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=cat).first().weight
                    CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=cat).update(weight=weight*DECREASE_RATE)
                ###############################

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

        # All eligable schedules
        queryset = Schedule.objects \
                    .filter(event__admin_approved=True) \
                    .filter(end_time__gte=timezone.now())

        # Filtering seen events
        if events_seen:
            for pk in events_seen:
                queryset = queryset.exclude(pk=pk)
        if self.request.user.is_authenticated:
            for schedule in queryset:
                my_interests = self.request.user.interested_events.all()
                if schedule in my_interests:
                    queryset = queryset.exclude(pk=schedule.id)
        # Anon user with multiple events
        if self.request.user.is_anonymous and events_seen:
            return queryset
        # No need to do selection
        elif len(queryset)<=1:
            return queryset
        ###############################
        # Base AI 4
        # Assign score to all schedules based on average category score.
        # Uses a weighted select to select what schedule to show.
        if self.request.user.is_authenticated:
            schedule_score = {}
            for schedule in queryset:
                sum = 0
                n = 0

                cats = schedule.event.interest_categories.all()
                if len(cats):
                    for cat in cats:
                        n+=1
                        sum += CategoryWeightsUser.objects.filter(user=self.request.user).filter(category=cat).first().weight
                    avg_score = sum/n
                else:
                    avg_score = np.random.uniform(0, 1)

                schedule_score[schedule.id] = avg_score

            sort_schedules = sorted(schedule_score.items(), key=lambda x: x[1], reverse=True)
            ids, scores =list(map(list, zip(*sort_schedules)))
            np_scores = np.array(scores)

            # Draws an ID based on weighted selection
            drawn_id = np.random.choice(ids, 1, p=(np_scores/np_scores.sum()))

        else: # Random
            schedule_id = np.zeros(len(queryset))
            for i, schedule in enumerate(queryset):
                schedule_id[i] = schedule.id
            drawn_id = np.random.choice(schedule_id)

        # Order our drawn ID up front. Requires an ordered list of queries.
        queryset = queryset.order_by(Case(When(pk=drawn_id, then=0), default=1))
        ###############################
        return queryset


class FinishSwipingView(TemplateView):
    template_name = "swiping/swipe_finish.html"
