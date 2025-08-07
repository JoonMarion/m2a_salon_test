from dal import autocomplete
from .models import Client, Service, Professional

class ClientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('get_queryset ClientAutocomplete chamado com q=', self.q)
        qs = Client.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class ServiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Service.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class ProfessionalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Professional.objects.all()

        if self.q:

            qs = qs.filter(name__icontains=self.q)
        return qs
