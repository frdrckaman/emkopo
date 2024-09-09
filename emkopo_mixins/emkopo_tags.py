from django import template

register = template.Library()


@register.filter(name='format_received_time')
def format_received_time(value):
    formated_dt = value.strftime('%d %b, %Y') if value else None
    return formated_dt
