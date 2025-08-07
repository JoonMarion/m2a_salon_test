from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def translate_status(value):
    mapping = {
        'scheduled': 'Agendado',
        'canceled': 'Cancelado',
        'completed': 'Concluído',
    }
    return mapping.get(value, value)


@register.filter
def status_badge_class(value):
    return {
        'scheduled': 'bg-warning',
        'canceled': 'bg-danger',
        'completed': 'bg-success',
    }.get(value, 'bg-secondary')

