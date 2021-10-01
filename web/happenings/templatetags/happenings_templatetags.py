from django import template

from ..models import Schedule, Event

register = template.Library()


@register.simple_tag
def get_event_times(schedule: Schedule):
    return schedule.get_times()


@register.simple_tag
def get_pricerange(event: Event):
    return event.get_pricerange()


@register.simple_tag
def get_schedules(event: Event):
    return Schedule.objects.filter(event=event)
