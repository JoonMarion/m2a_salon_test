from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

login_required_mixin = method_decorator(login_required, name='dispatch')

def translate_status(status):
    translations = {
        'scheduled': 'Agendado',
        'completed': 'Concluído',
        'canceled': 'Cancelado',
    }
    return translations.get(status, status)
