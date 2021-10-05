from django import template

from ..models import Schedule
from django.utils import timezone

register = template.Library()


@register.simple_tag
def get_event_times(event: Schedule):
    return event.get_times()


@register.simple_tag
def get_pricerange(schedule: Schedule):
    return schedule.event.get_pricerange()

@register.simple_tag
def set_current_date(shift_hours=0):
    return (timezone.now() + timezone.timedelta(hours=shift_hours)).strftime("%Y-%m-%d %H:%M")
