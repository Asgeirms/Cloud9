from django.contrib import admin
from .models import Event, Schedule, EventCategory, AccessibilityTag, CategoryWeightsUser, \
    GeneratedShortDescriptions


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'admin_approved')
    list_editable = ('admin_approved',)
    filter_horizontal = ('event_categories', 'accessibility_tags')


admin.site.register(Event, EventAdmin)
admin.site.register(Schedule)
admin.site.register(EventCategory)
admin.site.register(AccessibilityTag)
admin.site.register(CategoryWeightsUser)
admin.site.register(GeneratedShortDescriptions)
