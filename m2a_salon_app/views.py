from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date

from django.shortcuts import render, get_object_or_404, redirect

from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView

from django.urls import reverse_lazy, reverse
from django.utils.timezone import now

from datetime import datetime, timedelta
from .forms import ClientForm, ServiceForm, ProfessionalForm, AppointmentForm
from .models import Client, Service, Professional, Appointment
from .utils import login_required_mixin

import openpyxl


@login_required_mixin
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        date_str = self.request.GET.get('date')
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            selected_date = now().date()

        context['selected_date'] = selected_date
        context['prev_date'] = (selected_date - timedelta(days=1)).isoformat()
        context['next_date'] = (selected_date + timedelta(days=1)).isoformat()

        context['client_count'] = Client.objects.count()
        context['service_count'] = Service.objects.count()
        context['professional_count'] = Professional.objects.count()

        context['appointment_create_url'] = reverse_lazy('appointment-create')

        appointments = Appointment.objects.filter(
            scheduled_at__date=selected_date
        ).select_related('client', 'service', 'professional')

        context['appointments_today'] = appointments
        return context


@login_required_mixin
class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('home')
    template_name = 'components/modal_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Agendamento atualizado com sucesso!')
        return super().form_valid(form)


@login_required_mixin
class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('home')
    template_name = 'components/modal_confirm_delete.html'

    def form_valid(self, form):
        nome = str(self.object)
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name.capitalize()} "{nome}" excluído com sucesso!'
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@login_required_mixin
class ClientListView(ListView):
    model = Client
    context_object_name = 'clients'
    template_name = 'clients/list.html'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_form'] = ClientForm()
        context['client_create_url'] = reverse_lazy('client-create')

        context['edit_forms'] = {
            client.pk: {
                'form': ClientForm(instance=client),
                'modal_id': f'edit-client-modal{client.pk}',
                'action_update_url': reverse('client-update', kwargs={'pk': client.pk}),
            }
            for client in context['clients']
        }

        context['delete_modal'] = {
            client.pk: {
                'modal_id': f'delete-client-modal{client.pk}',
                'action_delete_url': reverse('client-delete', kwargs={'pk': client.pk}),
                'object_name': client.name,
            }
            for client in context['clients']
        }
        return context


@login_required_mixin
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client-list')
    template_name = 'clients/list.html'

    def form_valid(self, form):
        nome = str(self.object)
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name.capitalize()} "{nome}" excluído com sucesso!'
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@login_required_mixin
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/list.html'
    success_url = reverse_lazy('client-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


@login_required_mixin
class ServiceListView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'services/list.html'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_form'] = ServiceForm()
        context['service_create_url'] = reverse_lazy('service-create')

        context['edit_forms'] = {
            service.pk: {
                'form': ServiceForm(instance=service),
                'modal_id': f'edit-service-modal{service.pk}',
                'action_update_url': reverse('service-update', kwargs={'pk': service.pk}),
            }
            for service in context['services']
        }

        context['delete_modal'] = {
            service.pk: {
                'modal_id': f'delete-service-modal{service.pk}',
                'action_delete_url': reverse('service-delete', kwargs={'pk': service.pk}),
                'object_name': service.name
            }
            for service in context['services']
        }
        return context


@login_required_mixin
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/list.html'
    success_url = reverse_lazy('service-list')

    def form_valid(self, form):
        messages.success(self.request, 'Serviço atualizado com sucesso!')
        return super().form_valid(form)



@login_required_mixin
class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service-list')
    template_name = 'services/list.html'

    def form_valid(self, form):
        nome = str(self.object)
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name.capitalize()} "{nome}" excluído com sucesso!'
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@login_required_mixin
class ProfessionalListView(ListView):
    model = Professional
    template_name = 'professionals/list.html'
    context_object_name = 'professionals'
    paginate_by = 10
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professional_form'] = ProfessionalForm()
        context['professional_create_url'] = reverse_lazy('professional-create')

        context['edit_forms'] = {
            pro.pk: {
                'form': ProfessionalForm(instance=pro),
                'modal_id': f'edit-professional-modal{pro.pk}',
                'action_update_url': reverse('professional-update', kwargs={'pk': pro.pk}),
            }
            for pro in context['professionals']
        }

        context['delete_modal'] = {
            pro.pk: {
                'modal_id': f'delete-professional-modal{pro.pk}',
                'action_delete_url': reverse('professional-delete', kwargs={'pk': pro.pk}),
                'object_name': pro.name,
            }
            for pro in context['professionals']
        }
        return context


@login_required_mixin
class ProfessionalUpdateView(UpdateView):
    model = Professional
    form_class = ProfessionalForm
    template_name = 'professionals/list.html'
    success_url = reverse_lazy('professional-list')

    def form_valid(self, form):
        messages.success(self.request, 'Profissional atualizado com sucesso!')
        return super().form_valid(form)


@login_required_mixin
class ProfessionalDeleteView(DeleteView):
    model = Professional
    template_name = 'professionals/list.html'
    success_url = reverse_lazy('professional-list')

    def form_valid(self, form):
        nome = str(self.object)
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name.capitalize()} "{nome}" excluído com sucesso!'
        )
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@login_required_mixin
class GenericModalFormView(View):
    model = None
    form_class = None
    template_name = 'components/modal_form.html'
    success_url = reverse_lazy('home')

    def get(self, request, pk=None):
        instance = get_object_or_404(self.model, pk=pk) if pk else None
        form = self.form_class(instance=instance)
        return render(request, self.template_name, {'form': form, 'pk': pk})

    def post(self, request, pk=None):
        instance = get_object_or_404(self.model, pk=pk) if pk else None
        form = self.form_class(request.POST, instance=instance)

        if form.is_valid():
            obj = form.save()
            msg = (
                    f'{self.model._meta.verbose_name.capitalize()} '
                    + ('atualizado' if pk else 'criado')
                    + ' com sucesso!'
            )
            messages.success(request, msg)
            return redirect(self.success_url)

        if 'email' in form.errors:
            email_errors = form.errors['email']
            messages.error(request, email_errors.as_text().replace('* ', ''))
        else:
            messages.error(request, 'Erro ao salvar. Verifique os dados e tente novamente.')

        return redirect(self.success_url)


@login_required_mixin
class ClientModalView(GenericModalFormView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client-list')


@login_required_mixin
class ServiceModalView(GenericModalFormView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service-list')


@login_required_mixin
class ProfessionalModalView(GenericModalFormView):
    model = Professional
    form_class = ProfessionalForm
    success_url = reverse_lazy('professional-list')


@login_required_mixin
class AppointmentModalView(GenericModalFormView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy('home')


@login_required_mixin
class ReportCompletedAppointmentsView(TemplateView):
    template_name = 'reports/completed_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        try:
            start = parse_date(start_date) if start_date else now().date() - timedelta(days=30)
            end = parse_date(end_date) if end_date else now().date()
        except ValueError:
            start = now().date() - timedelta(days=30)
            end = now().date()

        completed_appointments = Appointment.objects.filter(
            status=Appointment.STATUS_COMPLETED,
            scheduled_at__date__range=(start, end)
        ).select_related('client', 'professional', 'service').order_by('scheduled_at')

        summary_by_professional = completed_appointments.values(
            'professional__name'
        ).annotate(total=Count('id')).order_by('-total')

        total_completed = completed_appointments.count()

        context.update({
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'total_completed': total_completed,
            'summary_by_professional': summary_by_professional,
            'completed_appointments': completed_appointments,
        })

        return context


@login_required_mixin
class ExportCompletedAppointmentsXLSXView(View):

    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        try:
            start = parse_date(start_date) if start_date else now().date() - timedelta(days=30)
            end = parse_date(end_date) if end_date else now().date()
        except ValueError:
            start = now().date() - timedelta(days=30)
            end = now().date()

        appointments = Appointment.objects.filter(
            status=Appointment.STATUS_COMPLETED,
            scheduled_at__date__range=(start, end)
        ).select_related('client', 'professional', 'service').order_by('scheduled_at')

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Agendamentos Concluídos"

        headers = ['Cliente', 'Serviço', 'Profissional', 'Data e Hora']
        ws.append(headers)

        for appt in appointments:
            ws.append([
                appt.client.name,
                appt.service.name,
                appt.professional.name,
                appt.scheduled_at.strftime('%d/%m/%Y %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=agendamentos_concluidos.xlsx'
        wb.save(response)
        return response


@login_required_mixin
class AppointmentEditFormAjaxView(View):
    def get(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)
        form = AppointmentForm(instance=appt)
        html = form.as_p()
        return JsonResponse({'form_html': html})


@login_required_mixin
class AppointmentDeleteDataAjaxView(View):
    def get(self, request, pk):
        appt = get_object_or_404(Appointment, pk=pk)
        object_name = f"{appt.client.name} - {appt.service.name} às {appt.scheduled_at.strftime('%H:%M')}"
        action_url = reverse('appointment-delete', kwargs={'pk': pk})
        return JsonResponse({'object_name': object_name, 'action_url': action_url})


@login_required_mixin
class AppointmentCreateAjaxView(View):
    def get(self, request):
        form = AppointmentForm()
        html = form.as_p()
        return JsonResponse({'form_html': html})