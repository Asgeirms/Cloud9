from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, CreateView, UpdateView

from adminpage.forms import GeneratedShortDescriptionsForm, InterestCategoryForm, RequirementCategoryForm
from happenings.models import Event, GeneratedShortDescriptions, InterestCategory, RequirementCategory


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

    template_name = "adminpage/create_description.html"
    models = GeneratedShortDescriptions
    form_class = GeneratedShortDescriptionsForm
    context_object_name = "description"
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class EditShortDescriptionView(PermissionRequiredMixin, UpdateView):
    """This is the view for editing premade short descriptions.
        The permission checks if the user is a staff user"""

    template_name = "adminpage/edit_description.html"
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


class InterestCategoryListView(PermissionRequiredMixin, ListView):
    """This is the list view for the interest categories.
            The permission check checks if the user is a staff user"""
    model = InterestCategory
    template_name = "adminpage/interest_categories.html"
    context_object_name = "categories"

    def has_permission(self):
        return self.request.user.is_staff


class CreateInterestCategory(PermissionRequiredMixin, CreateView):
    """This is the view for creating interest categories.
        The permission check ckecks if the user is a staff user"""

    template_name = "adminpage/create_interest_category.html"
    models = InterestCategory
    form_class = InterestCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class EditInterestCategory(PermissionRequiredMixin, UpdateView):
    """This is the view for editing interest categories.
            The permission checks if the user is a staff user"""

    template_name = "adminpage/edit_interest_category.html"
    model = InterestCategory
    form_class = InterestCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteInterestCategory(PermissionRequiredMixin, DeleteView):
    """This is the view for deleting interest categories.
            The permission check if the user is a staff user"""

    model = InterestCategory
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class RequirementCategoryListView(PermissionRequiredMixin, ListView):
    """This is the list view for the requirement categories.
            The permission check checks if the user is a staff user"""

    model = RequirementCategory
    template_name = "adminpage/requirement_categories.html"
    context_object_name = "categories"

    def has_permission(self):
        return self.request.user.is_staff


class CreateRequirementCategory(PermissionRequiredMixin, CreateView):
    """This is the view for creating requirement categories.
        The permission check ckecks if the user is a staff user"""

    template_name = "adminpage/create_requirement_category.html"
    models = RequirementCategory
    form_class = RequirementCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff


class EditRequirementCategory(PermissionRequiredMixin, UpdateView):
    """This is the view for editing requirement categories.
            The permission checks if the user is a staff user"""

    template_name = "adminpage/edit_requirement_category.html"
    model = RequirementCategory
    form_class = RequirementCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteRequirementCategory(PermissionRequiredMixin, DeleteView):
    """This is the view for deleting requirement categories.
            The permission check if the user is a staff user"""

    model = RequirementCategory
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff
