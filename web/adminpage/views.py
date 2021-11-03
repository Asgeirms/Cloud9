from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, CreateView, UpdateView

from adminpage.forms import GeneratedShortDescriptionsForm, InterestCategoryForm, RequirementCategoryForm
from happenings.models import Event, GeneratedShortDescriptions, InterestCategory, RequirementCategory


class AdminpanelView(PermissionRequiredMixin, TemplateView):
    template_name="adminpage/adminpage.html"

    def has_permission(self):
        return self.request.user.is_staff


class CurateEventsView(PermissionRequiredMixin, ListView):
    template_name = "adminpage/curate_events.html"
    context_object_name = "events"

    def get_queryset(self):
        data = {
            "pending": Event.objects.filter(admin_approved='P'),
            "not_approved": Event.objects.filter(admin_approved='N'),
            "approved": Event.objects.filter(admin_approved='A'),
            "deleted": Event.objects.filter(admin_approved='D')
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
        event.admin_approved = 'N'
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def approve(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = 'A'
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def delete(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = 'D'
        event.save()
        return redirect('curate_events')

    @user_passes_test(lambda user: user.is_staff)
    def restore(self, pk):
        event = Event.objects.get(pk=pk)
        event.admin_approved = 'P'
        event.save()
        return redirect('curate_events')


class DeleteEventAdminView(PermissionRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('curate_events')

    def has_permission(self):
        return self.request.user.is_staff


class ShortDescriptionListView(PermissionRequiredMixin, ListView):
    model = GeneratedShortDescriptions
    template_name = "adminpage/descriptions_list.html"
    context_object_name = "descriptions"

    def has_permission(self):
        return self.request.user.is_staff


class CreateShortDescriptionView(PermissionRequiredMixin, CreateView):
    template_name = "adminpage/create_description.html"
    models = GeneratedShortDescriptions
    form_class = GeneratedShortDescriptionsForm
    context_object_name = "description"
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class EditShortDescriptionView(PermissionRequiredMixin, UpdateView):
    template_name = "adminpage/edit_description.html"
    model = GeneratedShortDescriptions
    form_class = GeneratedShortDescriptionsForm
    context_object_name = "description"
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteShortDescriptionView(PermissionRequiredMixin, DeleteView):
    model = GeneratedShortDescriptions
    success_url = reverse_lazy('descriptions')

    def has_permission(self):
        return self.request.user.is_staff


class InterestCategoryListView(PermissionRequiredMixin, ListView):
    model = InterestCategory
    template_name = "adminpage/interest_categories.html"
    context_object_name = "categories"

    def has_permission(self):
        return self.request.user.is_staff


class CreateInterestCategory(PermissionRequiredMixin, CreateView):
    template_name = "adminpage/create_interest_category.html"
    models = InterestCategory
    form_class = InterestCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class EditInterestCategory(PermissionRequiredMixin, UpdateView):
    template_name = "adminpage/edit_interest_category.html"
    model = InterestCategory
    form_class = InterestCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteInterestCategory(PermissionRequiredMixin, DeleteView):
    model = InterestCategory
    success_url = reverse_lazy('interest_categories')

    def has_permission(self):
        return self.request.user.is_staff


class RequirementCategoryListView(PermissionRequiredMixin, ListView):
    model = RequirementCategory
    template_name = "adminpage/requirement_categories.html"
    context_object_name = "categories"

    def has_permission(self):
        return self.request.user.is_staff


class CreateRequirementCategory(PermissionRequiredMixin, CreateView):
    template_name = "adminpage/create_requirement_category.html"
    models = RequirementCategory
    form_class = RequirementCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff


class EditRequirementCategory(PermissionRequiredMixin, UpdateView):
    template_name = "adminpage/edit_requirement_category.html"
    model = RequirementCategory
    form_class = RequirementCategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff


class DeleteRequirementCategory(PermissionRequiredMixin, DeleteView):
    model = RequirementCategory
    success_url = reverse_lazy('requirement_categories')

    def has_permission(self):
        return self.request.user.is_staff
