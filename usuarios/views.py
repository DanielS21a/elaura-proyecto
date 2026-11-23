from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Gerente').exists():
            # poner la ruta del gerente cuando este lista
            return reverse_lazy('panel')
        if user.groups.filter(name='Recepcionista').exists():
            # poner la ruta del recepcionista cuando este lista
            return reverse_lazy('panel')
        return reverse_lazy('panel')


class UsuarioLogoutView(LogoutView):
    next_page = reverse_lazy('login')


@login_required
def panel_view(request):
    user = request.user
    if user.groups.filter(name='Gerente').exists():
        rol = 'Gerente'
    elif user.groups.filter(name='Recepcionista').exists():
        rol = 'Recepcionista'
    elif user.is_superuser:
        rol = 'Superusuario'
    else:
        rol = 'Sin rol asignado'

    return render(request, 'usuarios/panel.html', {'rol': rol})
