import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from m2a_salon_app.models import Client, Service, Professional, Appointment

class Command(BaseCommand):
    help = 'Popula o banco com muitos dados para teste'

    def handle(self, *args, **options):
        fake = Faker('pt_BR')

        self.stdout.write('Apagando dados antigos...')
        Appointment.objects.all().delete()
        Professional.objects.all().delete()
        Client.objects.all().delete()
        Service.objects.all().delete()

        self.stdout.write('Criando serviços...')
        service_names = [
            'Corte de cabelo', 'Pintura de cabelo', 'Escova', 'Manicure', 'Pedicure',
            'Limpeza de pele', 'Depilação', 'Maquiagem', 'Tratamento capilar', 'Penteado',
            'Massagem relaxante', 'Coloração', 'Alisamento', 'Hidratação', 'Design de sobrancelhas'
        ]
        services = []
        for name in service_names:
            service = Service.objects.create(
                name=name,
                duration_minutes=random.choice([15, 30, 45, 60, 90]),
                price=round(random.uniform(30, 500), 2)
            )
            services.append(service)

        self.stdout.write('Criando profissionais...')
        professionals = []
        for _ in range(200):
            pro = Professional.objects.create(
                name=fake.name(),
                is_active=True
            )
            pro.specialties.set(random.sample(services, random.randint(1, 5)))
            professionals.append(pro)

        self.stdout.write('Criando clientes...')
        clients = []
        for _ in range(1000):
            client = Client.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number()
            )
            clients.append(client)

        self.stdout.write('Criando agendamentos...')
        statuses = [Appointment.STATUS_SCHEDULED, Appointment.STATUS_COMPLETED, Appointment.STATUS_CANCELED]

        base_date = datetime.now()

        appointments_to_create = []
        created_count = 0
        max_appointments = 2000

        while created_count < max_appointments:
            client = random.choice(clients)
            service = random.choice(services)
            eligible_pros = [p for p in professionals if service in p.specialties.all()]
            if not eligible_pros:
                continue
            professional = random.choice(eligible_pros)

            scheduled_at = base_date - timedelta(days=random.randint(0, 90), hours=random.randint(8, 20))

            status = random.choices(
                population=statuses,
                weights=[0.3, 0.5, 0.2],
                k=1
            )[0]

            appointment = Appointment(
                client=client,
                service=service,
                professional=professional,
                scheduled_at=scheduled_at,
                status=status
            )
            appointments_to_create.append(appointment)
            created_count += 1

            if len(appointments_to_create) >= 500:
                Appointment.objects.bulk_create(appointments_to_create)
                appointments_to_create = []
                self.stdout.write(f'{created_count} agendamentos criados...')

        if appointments_to_create:
            Appointment.objects.bulk_create(appointments_to_create)

        self.stdout.write(self.style.SUCCESS(f'Total de {created_count} agendamentos criados com sucesso!'))
