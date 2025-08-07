from django.urls import path, include, re_path

from .views import HomeView
from .views import ClientListView, ClientModalView, ClientUpdateView, ClientDeleteView
from .views import ServiceListView, ServiceModalView, ServiceUpdateView, ServiceDeleteView
from .views import ProfessionalListView, ProfessionalModalView, ProfessionalUpdateView, ProfessionalDeleteView
from .views import AppointmentModalView, AppointmentUpdateView, AppointmentDeleteView, AppointmentEditFormAjaxView, \
    AppointmentDeleteDataAjaxView, AppointmentCreateAjaxView
from .views import ReportCompletedAppointmentsView, ExportCompletedAppointmentsXLSXView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('appointment/create/data', AppointmentCreateAjaxView.as_view(), name='appointment-create-ajax'),
    path('appointment/create/', AppointmentModalView.as_view(), name='appointment-create'),

    path('appointment/update-form/<int:pk>/', AppointmentEditFormAjaxView.as_view(), name='appointment-update-form-ajax'),
    path('appointment/update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),

    path('appointment/delete-data/<int:pk>/', AppointmentDeleteDataAjaxView.as_view(),name='appointment-delete-data-ajax'),
    path('appointment/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment-delete'),


    path('clients/', ClientListView.as_view(), name='client-list'),
    path('client/create/', ClientModalView.as_view(), name='client-create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),

    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service/create/', ServiceModalView.as_view(), name='service-create'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='service-update'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='service-delete'),

    path('professionals/', ProfessionalListView.as_view(), name='professional-list'),
    path('professional/create/', ProfessionalModalView.as_view(), name='professional-create'),
    path('professional/update/<int:pk>/', ProfessionalModalView.as_view(), name='professional-update'),
    path('professional/delete/<int:pk>/', ProfessionalDeleteView.as_view(), name='professional-delete'),

    path('reports/completed/', ReportCompletedAppointmentsView.as_view(), name='report-completed'),
    path('reports/completed-appointments/xlsx/', ExportCompletedAppointmentsXLSXView.as_view(), name='report-completed-appointments-xlsx'),
]
