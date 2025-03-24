from django import template
from django.utils.formats import date_format
from django.utils.timezone import localtime
from datetime import datetime

register = template.Library()

@register.filter(name='spanish_date')
def spanish_date(value):
    if not value:
        return ''
    
    months = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    
    if isinstance(value, datetime):
        value = value.date()
    
    day = value.day
    month = months[value.month]
    year = value.year
    
    return f"{day} de {month} de {year}"