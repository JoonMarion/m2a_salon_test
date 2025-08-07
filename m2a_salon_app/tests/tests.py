from django.test import TestCase
from django.utils import timezone
from m2a_salon_app.models import Client, Service, Professional, Appointment


class ModelTests(TestCase):

    def setUp(self):
        self.client = Client.objects.create(
            name='Maria Silva',
            email='maria@example.com',
            phone='11999999999'
        )
        self.service = Service.objects.create(
            name='Corte de cabelo',
            duration_minutes=30,
            price=50.00
        )
        self.professional = Professional.objects.create(
            name='João Barber'
        )
        self.professional.specialties.add(self.service)

    def test_client_str(self):
        self.assertEqual(str(self.client), 'Maria Silva')

    def test_service_str(self):
        self.assertEqual(str(self.service), 'Corte de cabelo')

    def test_professional_str(self):
        self.assertEqual(str(self.professional), 'João Barber')

    def test_professional_specialties(self):
        self.assertIn(self.service, self.professional.specialties.all())

    def test_appointment_creation(self):
        scheduled_time = timezone.now() + timezone.timedelta(days=1)
        appointment = Appointment.objects.create(
            client=self.client,
            service=self.service,
            professional=self.professional,
            scheduled_at=scheduled_time
        )
        self.assertEqual(appointment.status, Appointment.STATUS_SCHEDULED)
        self.assertEqual(str(appointment), f"Maria Silva — Corte de cabelo em {scheduled_time:%d/%m/%Y %H:%M}")

    def test_cascade_delete_client(self):
        appointment = Appointment.objects.create(
            client=self.client,
            service=self.service,
            professional=self.professional,
            scheduled_at=timezone.now() + timezone.timedelta(days=1)
        )
        self.client.delete()
        self.assertEqual(Appointment.objects.count(), 0)

    def test_cascade_delete_service(self):
        appointment = Appointment.objects.create(
            client=self.client,
            service=self.service,
            professional=self.professional,
            scheduled_at=timezone.now() + timezone.timedelta(days=1)
        )
        self.service.delete()
        self.assertEqual(Appointment.objects.count(), 0)

    def test_cascade_delete_professional(self):
        appointment = Appointment.objects.create(
            client=self.client,
            service=self.service,
            professional=self.professional,
            scheduled_at=timezone.now() + timezone.timedelta(days=1)
        )
        self.professional.delete()
        self.assertEqual(Appointment.objects.count(), 0)
