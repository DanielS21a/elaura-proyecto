from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    # Mientras no exista una portada, el inicio lleva al listado de habitaciones.
    path('', RedirectView.as_view(pattern_name='habitaciones:lista'), name='inicio'),
    path('habitaciones/', include('habitaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
]
