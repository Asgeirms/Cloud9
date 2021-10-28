from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

# Create your views here.
from django.views.generic import ListView, DetailView

from happenings.models import Event


class CurateEventsView(PermissionRequiredMixin, ListView):
    template_name = "adminpage/curate_events.html"
    context_object_name = "events"

    def get_queryset(self):
        data = {
            "not_approved": Event.objects.filter(admin_approved=False),
            "approved": Event.objects.filter(admin_approved=True)
        }
        return data

    def has_permission(self):
        return self.request.user.is_staff


class AdminEventDetailView(PermissionRequiredMixin, DetailView):
    template_name = "adminpage/admin_event_detail_view.html"
    model = Event
    context_object_name = "event"

    def has_permission(self):
        return self.request.user.is_staff

    @user_passes_test(lambda user: user.is_staff)
    def disapprove(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = False
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def approve(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = True
        event.save()
        return redirect('curate_events')
