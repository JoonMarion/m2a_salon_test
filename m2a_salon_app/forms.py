from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Client, Service, Professional, Appointment

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']
        labels = {
            'name': _('Nome'),
            'email': _('E-mail'),
            'phone': _('Telefone'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome completo'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('seu@exemplo.com'),
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('(XX) XXXXX-XXXX'),
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Client.objects.filter(email=email)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError(_('Já existe um cliente com este e-mail.'))

        return email


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'duration_minutes', 'price']
        labels = {
            'name': _('Serviço'),
            'duration_minutes': _('Duração (minutos)'),
            'price': _('Preço (R$)'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do serviço'),
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Duração em minutos'),
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('Preço (R$)'),
                'step': '0.01',
            }),
        }


class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['name', 'specialties', 'is_active']
        labels = {
            'name': _('Nome'),
            'specialties': _('Especialidades'),
            'is_active': _('Ativo'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Nome do profissional'),
            }),
            'specialties': forms.CheckboxSelectMultiple(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(self.fields['specialties'].widget, forms.CheckboxSelectMultiple):
            self.fields['specialties'].widget.attrs.update({
                'class': 'form-check',
            })

        for option in self.fields['specialties'].widget.choices:
            pass


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['client', 'service', 'professional', 'scheduled_at', 'status']
        widgets = {
            'scheduled_at': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['client'].queryset = Client.objects.order_by('name')
        self.fields['service'].queryset = Service.objects.order_by('name')
        self.fields['professional'].queryset = Professional.objects.order_by('name')

        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['service'].widget.attrs.update({'class': 'form-control'})
        self.fields['professional'].widget.attrs.update({'class': 'form-control'})

        self.fields['status'].choices = [
            (Appointment.STATUS_SCHEDULED, _('Agendado')),
            (Appointment.STATUS_COMPLETED, _('Concluído')),
            (Appointment.STATUS_CANCELED, _('Cancelado')),
        ]