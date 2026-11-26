from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from usuarios.mixins import GerenteRequeridoMixin, PersonalRequeridoMixin

from . import services
from .forms import HabitacionForm
from .models import Habitacion


class HabitacionListView(PersonalRequeridoMixin, ListView):
    template_name = 'habitaciones/lista.html'
    context_object_name = 'habitaciones'

    def get_queryset(self):
        return services.listar_habitaciones()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habitaciones = context['habitaciones']
        vacantes = sum(h.esta_vacante() for h in habitaciones)
        context.update(
            total=len(habitaciones),
            vacantes=vacantes,
            ocupadas=len(habitaciones) - vacantes,
            capacidad_total=sum(h.capacidad for h in habitaciones),
            orientaciones=Habitacion.Orientacion.choices,
            estados=Habitacion.Disponibilidad.choices,
        )
        return context


class HabitacionCreateView(GerenteRequeridoMixin, FormView):
    template_name = 'habitaciones/registrar.html'
    form_class = HabitacionForm
    success_url = reverse_lazy('habitaciones:lista')

    def form_valid(self, form):
        try:
            habitacion = services.registrar_habitacion(
                gerente=self.request.user, **form.cleaned_data
            )
        except services.NumeroDuplicadoError:
            form.add_error('numero', 'Ya existe una habitación con este número.')
            return self.form_invalid(form)
        messages.success(
            self.request, f'La habitación {habitacion.numero} se registró correctamente.'
        )
        if 'guardar_y_agregar' in self.request.POST:
            return redirect('habitaciones:registrar')
        return redirect(self.get_success_url())
