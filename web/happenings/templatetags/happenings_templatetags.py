from django import template

from ..models import Schedule

register = template.Library()


@register.simple_tag
def get_event_times(event: Schedule):
    return event.get_times()


@register.simple_tag
def get_pricerange(Schedule: Schedule):
    return Schedule.event.get_pricerange()
