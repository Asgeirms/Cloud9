from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView

from happenings.models import Event, Schedule


class CurateEventsView(UserPassesTestMixin, ListView):
    template_name = "adminpage/curate_events.html"
    context_object_name = "events"

    def get_queryset(self):
        data = {
            "not_approved": Event.objects.filter(admin_approved=False),
            "approved": Event.objects.filter(admin_approved=True)
        }
        return data

    def test_func(self):
        return self.request.user.is_staff


class AdminEventDetailView(UserPassesTestMixin, DetailView):
    template_name = "adminpage/detail_event_view.html"
    model = Event
    context_object_name = "event"

    def test_func(self):
        return self.request.user.is_staff

    @user_passes_test(lambda user: user.is_staff)
    def disapprove(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = False
        event.save()
        return redirect('curateEvents')

    @user_passes_test(lambda user: user.is_staff)
    def approve(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = True
        event.save()
        return redirect('curateEvents')
