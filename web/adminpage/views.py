from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, CreateView, UpdateView

from adminpage.forms import GeneratedShortDescriptionsForm, EventCategoryForm, AccessibilityTagForm
from happenings.models import Event, GeneratedShortDescriptions, EventCategory, AccessibilityTag


class AdminpanelView(PermissionRequiredMixin, TemplateView):
    """This is the view for the adminpanel,
        the premission is used to check if the user is a staff member"""

    template_name="adminpage/adminpage.html"

    def has_permission(self):
        return self.request.user.is_staff


class CurateEventsView(PermissionRequiredMixin, ListView):
    """This is the view for the curation panel,
        the data is separated into the different admin_approved statuses,
        the permission is used to check if the user is a staff member"""

    template_name = "adminpage/curate_events.html"
    context_object_name = "events"

    def get_queryset(self):
        data = {
            "pending": Event.objects.filter(admin_approved=Event.Status.PENDING),
            "not_approved": Event.objects.filter(admin_approved=Event.Status.DISAPPROVED),
            "approved": Event.objects.filter(admin_approved=Event.Status.APPROVED),
            "deleted": Event.objects.filter(admin_approved=Event.Status.DELETED)
        }
        return data

    def has_permission(self):
        return self.request.user.is_staff


class AdminEventDetailView(PermissionRequiredMixin, DetailView):
    """This is the view for the detailed view for an event, shown via the adminpage,
        the permission checks if the user is a staff user.
        The different functions change the status of the event"""

    template_name = "adminpage/admin_event_detail_view.html"
    model = Event
    context_object_name = "event"

    def has_permission(self):
        return self.request.user.is_staff

    @user_passes_test(lambda user: user.is_staff)
    def disapprove(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = Event.Status.DISAPPROVED
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def approve(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = Event.Status.APPROVED
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def delete(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = Event.Status.DELETED
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def restore(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = Event.Status.PENDING
        event.save()
        return redirect('curate_events')


class DeleteEventAdminView(PermissionRequiredMixin, DeleteView):
    """
        This is the view for deleting an event via the admin pages.
        The permission checks if the user is a staff user
    """

    model = Event
    success_url = reverse_lazy('curate_events')

    def has_permission(self):
        return self.request.user.is_staff


class ShortDescriptionListView(PermissionRequiredMixin, ListView):
    """This is the list view for the premade short descriptions.
        The permission check checks if the user is a staff user"""

    model = GeneratedShortDescriptions
    template_name = "adminpage/descriptions_list.html"
    context_object_name = "descriptions"

    def has_permission(self):
        return self.request.user.is_staff


class CreateShortDescriptionView(PermissionRequiredMixin, CreateView):
    """This is the view for creating premade short descriptions.
        The permission check ckecks if the user is a staff user"""

    template_name = "adminpage/description_create.html"
    models = GeneratedShortDescriptions
    form_class = GeneratedShortDescriptionsForm
    context_object_name = "description"
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class EditShortDescriptionView(PermissionRequiredMixin, UpdateView):
    """This is the view for editing premade short descriptions.
        The permission checks if the user is a staff user"""

    template_name = "adminpage/description_edit.html"
    model = GeneratedShortDescriptions
    form_class = GeneratedShortDescriptionsForm
    context_object_name = "description"
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteShortDescriptionView(PermissionRequiredMixin, DeleteView):
    """This is the view for deleting premade short descriptions.
        The permission check if the user is a staff user"""

    model = GeneratedShortDescriptions
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class EventCategoryListView(PermissionRequiredMixin, ListView):
    """This is the list view for the event categories.
            The permission check checks if the user is a staff user"""
    model = EventCategory
    template_name = "adminpage/event_categories_list.html"
    context_object_name = "categories"

    def has_permission(self):
        return self.request.user.is_staff


class CreateEventCategory(PermissionRequiredMixin, CreateView):
    """This is the view for creating event categories.
        The permission check ckecks if the user is a staff user"""

    template_name = "adminpage/event_category_create.html"
    models = EventCategory
    form_class = EventCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('event_categories')

    def has_permission(self):
        return self.request.user.is_staff


class EditEventCategory(PermissionRequiredMixin, UpdateView):
    """This is the view for editing event categories.
            The permission checks if the user is a staff user"""

    template_name = "adminpage/event_category_edit.html"
    model = EventCategory
    form_class = EventCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('event_categories')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteEventCategory(PermissionRequiredMixin, DeleteView):
    """This is the view for deleting event categories.
            The permission check if the user is a staff user"""

    model = EventCategory
    success_url = reverse_lazy('event_categories')

    def has_permission(self):
        return self.request.user.is_staff


class AccessibilityTagsListView(PermissionRequiredMixin, ListView):
    """This is the list view for the accessibility tags.
            The permission check checks if the user is a staff user"""

    model = AccessibilityTag
    template_name = "adminpage/accessibility_tags_list.html"
    context_object_name = "tags"

    def has_permission(self):
        return self.request.user.is_staff


class CreateAccessibilityTag(PermissionRequiredMixin, CreateView):
    """This is the view for creating accessibility tags.
        The permission check ckecks if the user is a staff user"""

    template_name = "adminpage/accessibility_tag_create.html"
    models = AccessibilityTag
    form_class = AccessibilityTagForm
    context_object_name = "tag"
    success_url = reverse_lazy('accessibility_tags')

    def has_permission(self):
        return self.request.user.is_staff


class EditAccessibilityTag(PermissionRequiredMixin, UpdateView):
    """This is the view for editing accessibility tags.
            The permission checks if the user is a staff user"""

    template_name = "adminpage/accessibility_tag_edit.html"
    model = AccessibilityTag
    form_class = AccessibilityTagForm
    context_object_name = "tag"
    success_url = reverse_lazy('accessibility_tags')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteAccessibilityTag(PermissionRequiredMixin, DeleteView):
    """This is the view for deleting accessibility tags.
            The permission check if the user is a staff user"""

    model = AccessibilityTag
    success_url = reverse_lazy('accessibility_tags')

    def has_permission(self):
        return self.request.user.is_staff
