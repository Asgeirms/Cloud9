from django import template

from ..models import Schedule, Event
from django.utils import timezone

register = template.Library()


@register.simple_tag
def get_event_times(schedule: Schedule):
    return schedule.get_times()


@register.simple_tag
def get_pricerange(event: Event):
    return event.get_pricerange()


@register.simple_tag
def get_schedules(event: Event):
    return Schedule.objects.filter(event=event).order_by('start_time')


@register.simple_tag
def set_current_date(shift_hours=0):
    return (timezone.now() + timezone.timedelta(hours=shift_hours)).strftime("%Y-%m-%d %H:%M")
