from django.urls import path

from . import views

app_name = 'habitaciones'

urlpatterns = [
    path('', views.HabitacionListView.as_view(), name='lista'),
    path('registrar/', views.HabitacionCreateView.as_view(), name='registrar'),
]
