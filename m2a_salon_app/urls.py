from django.urls import path, include, re_path
from .autocompletes import ClientAutocomplete, ServiceAutocomplete, ProfessionalAutocomplete

from .views import HomeView, ReportCompletedAppointmentsView
from .views import ClientListView, ClientModalView, ClientUpdateView, ClientDeleteView
from .views import ServiceListView, ServiceModalView, ServiceUpdateView, ServiceDeleteView
from .views import ProfessionalListView, ProfessionalModalView, ProfessionalUpdateView, ProfessionalDeleteView
from .views import AppointmentModalView, AppointmentUpdateView, AppointmentDeleteView, AppointmentEditFormAjaxView, \
    AppointmentDeleteDataAjaxView, AppointmentCreateAjaxView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('appointment/create/data', AppointmentCreateAjaxView.as_view(), name='appointment-create-ajax'),
    path('appointment/create/', AppointmentModalView.as_view(), name='appointment-create'),

    path('appointments/<int:pk>/update-form/', AppointmentEditFormAjaxView.as_view(), name='appointment-update-form-ajax'),
    path('appointment/update/<int:pk>/', AppointmentUpdateView.as_view(), name='appointment-update'),

    path('appointments/<int:pk>/delete-data/', AppointmentDeleteDataAjaxView.as_view(),name='appointment-delete-data-ajax'),
    path('appointment/delete/<int:pk>/', AppointmentDeleteView.as_view(), name='appointment-delete'),


    path('clients/', ClientListView.as_view(), name='client-list'),
    path('client/create/', ClientModalView.as_view(), name='client-create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),
    path('client-autocomplete/', ClientAutocomplete.as_view(), name='client-autocomplete'),

    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service/create/', ServiceModalView.as_view(), name='service-create'),
    path('service/update/<int:pk>/', ServiceUpdateView.as_view(), name='service-update'),
    path('service/delete/<int:pk>/', ServiceDeleteView.as_view(), name='service-delete'),
    re_path(r'^service-autocomplete/$', ServiceAutocomplete.as_view(), name='service-autocomplete'),

    path('professionals/', ProfessionalListView.as_view(), name='professional-list'),
    path('professional/create/', ProfessionalModalView.as_view(), name='professional-create'),
    path('professional/update/<int:pk>/', ProfessionalModalView.as_view(), name='professional-update'),
    path('professional/delete/<int:pk>/', ProfessionalDeleteView.as_view(), name='professional-delete'),
    re_path(r'^professional-autocomplete/$', ProfessionalAutocomplete.as_view(), name='professional-autocomplete'),

    path('relatorio/concluidos/', ReportCompletedAppointmentsView.as_view(), name='report-completed'),
]
