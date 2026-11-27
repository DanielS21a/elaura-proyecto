from django.urls import path
from .views import RegistrarPersonalView, UsuarioLoginView, UsuarioLogoutView, panel_view

urlpatterns = [
    path('', panel_view, name='home'),
    path('panel/', panel_view, name='panel'),
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
    path('usuarios/registrar/', RegistrarPersonalView.as_view(), name='registrar_personal'),
]
