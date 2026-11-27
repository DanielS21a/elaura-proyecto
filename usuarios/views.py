from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegistrarPersonalForm
from .mixins import GerenteRequeridoMixin


class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True
    # Destino por defecto tras iniciar sesión. Si la URL trae ?next=..., LoginView
    # respeta ese destino (por ejemplo, al llegar redirigido desde /habitaciones/registrar/).
    next_page = reverse_lazy('habitaciones:lista')


class UsuarioLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def panel_view(request):
    # get_rol_display() devuelve la etiqueta legible del choice ('Gerente', 'Recepcionista').
    rol = request.user.get_rol_display() or 'Sin rol asignado'
    return render(request, 'usuarios/panel.html', {'rol': rol})


class RegistrarPersonalView(GerenteRequeridoMixin, FormView):
    template_name = 'usuarios/registrar_personal.html'
    form_class = RegistrarPersonalForm
    success_url = reverse_lazy('registrar_personal')

    def form_valid(self, form):
        usuario = form.save()
        messages.success(
            self.request,
            f'Usuario "{usuario.username}" creado correctamente con el rol {usuario.get_rol_display()}.',
        )
        return super().form_valid(form)
