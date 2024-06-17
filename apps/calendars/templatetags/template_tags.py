import datetime
from genericpath import exists
from django import template
from django.utils import timezone
from ..models import PERIOD

register = template.Library()


@register.filter(name='html_attributes')
def html_attributes(value, arg):
    """ Allows adding of attributes to tagged form elements. """
    attrs = value.field.widget.attrs
    components = arg.split(',')

    for string in components:
        key, values_string = string.split(':')
        values = values_string.strip()

        if attrs.get(key):
            values = f'{attrs.get(key)} {values}'

        attrs.update({key: values})

    return str(value)


@register.simple_tag
def current_datetime(zone, format_string):
    from django.utils import timezone
    from platform import python_version
    import sys
    # Only for python <= 3.8 . For newest release use import zoneinfo from python default package
    if sys.version_info <= (3, 8):
        import backports.zoneinfo as zoneinfo
    else:
         import zoneinfo

    timezone.activate(zoneinfo.ZoneInfo(zone))
    current_tz = timezone.get_current_timezone()
    local = timezone.localtime(timezone.now()).astimezone(current_tz)

    return local.strftime(format_string)  # timezone.localtime(timezone.now()).strftime(format_string)  # datetime.datetime.now().strftime(format_string)


@register.filter(name='forloop_range')
def forloop_range(max_val):
    return range(max_val)


@register.simple_tag
def month_fr(month_en):
    if month_en == 'January':
        return 'Janvier'
    elif month_en == 'February':
        return 'Février'
    elif month_en == 'March':
        return 'Mars'
    elif month_en == 'April':
        return 'Avril'
    elif month_en == 'May':
        return 'Mai'
    elif month_en == 'June':
        return 'Juin'
    elif month_en == 'July':
        return 'Juillet'
    elif month_en == 'August':
        return 'Août'
    elif month_en == 'September':
        return 'Septembre'
    elif month_en == 'October':
        return 'Octobre'
    elif month_en == 'November':
        return 'Novembre'
    elif month_en == 'December':
        return 'Décembre'
    else:
        return '---'


@register.simple_tag
def time_conversion_tag(input_time, input_unit, output_unit):
    from decimal import Decimal
    hour_by_day = 0

    if hour_by_day and hour_by_day is not None:
        if input_unit == PERIOD.DAY and output_unit == PERIOD.HOUR:
            return round(Decimal(input_time) * Decimal(hour_by_day), 2)
        elif input_unit == PERIOD.HOUR and output_unit == PERIOD.DAY:
            return round(Decimal(input_time) / Decimal(hour_by_day), 2) 
    
    return round(Decimal(input_time), 2)


@register.simple_tag
def day_hours(): 
    return 8


register.filter('html_attributes', html_attributes)
register.filter('forloop_range', forloop_range)
