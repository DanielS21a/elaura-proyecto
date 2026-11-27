from django.contrib import admin
from django.urls import include, path

from .views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='inicio'),
    path('habitaciones/', include('habitaciones.urls')),
    path('usuarios/', include('usuarios.urls')),
]
