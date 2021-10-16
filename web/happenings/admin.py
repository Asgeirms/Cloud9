from django.contrib import admin
from .models import Event, Schedule, InterestCategory, RequirementCategory, CategoryWeightsUser


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'admin_approved')
    list_editable = ('admin_approved',)
    filter_horizontal = ('interest_categories', 'requirement_categories')


admin.site.register(Event, EventAdmin)
admin.site.register(Schedule)
admin.site.register(InterestCategory)
admin.site.register(RequirementCategory)
admin.site.register(CategoryWeightsUser)
