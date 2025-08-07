from django.contrib import admin
from .models import Client, Service, Professional, Appointment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'specialties')
    filter_horizontal = ('specialties',)  # Para melhorar o M2M no admin


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'professional', 'scheduled_at', 'status', 'created_at')
    search_fields = ('client__name', 'professional__name', 'service__name')
    list_filter = ('status', 'scheduled_at', 'professional')
    ordering = ('-scheduled_at',)
    autocomplete_fields = ('client', 'service', 'professional')
