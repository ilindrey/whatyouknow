from dateutil.relativedelta import relativedelta

from django import template
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.utils.timezone import now


register = template.Library()


@register.filter
def datetime_format(value):
    month = now() - relativedelta(months=+1)
    if value < month:
        return date(value, r'M d, Y \a\t h:i A')
    else:
        return timesince(value)
