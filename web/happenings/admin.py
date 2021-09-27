from django.contrib import admin
from .models import Event, Schedule


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'admin_approved')
    list_editable = ('admin_approved',)


admin.site.register(Event, EventAdmin)
admin.site.register(Schedule)
