from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('interested_events',)}),
    )
    filter_horizontal = ('interested_events',)


admin.site.register(User, CustomUserAdmin)
