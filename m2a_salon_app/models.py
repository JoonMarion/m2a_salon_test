from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Serviço')
        verbose_name_plural = _('Serviços')


class Professional(models.Model):
    name = models.CharField(max_length=100)
    specialties = models.ManyToManyField(Service, related_name='professionals')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Profissional')
        verbose_name_plural = _('Profissionais')


class Appointment(models.Model):
    STATUS_SCHEDULED = 'scheduled'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, 'Scheduled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELED, 'Canceled'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='appointments')
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Agendamento')
        verbose_name_plural = _('Agendamentos')
        ordering = ['scheduled_at']
        indexes = [
            models.Index(fields=['professional', 'scheduled_at']),
        ]

    def __str__(self):
        return _("{client} — {service} em {dt:%d/%m/%Y %H:%M}").format(
            client=self.client.name,
            service=self.service.name,
            dt=self.scheduled_at
        )