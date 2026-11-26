from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


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
