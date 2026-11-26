from django import forms

from .models import Habitacion


class HabitacionForm(forms.ModelForm):
    # Se declara aparte para no incluir la opción vacía entre los botones.
    orientacion = forms.ChoiceField(
        label='Orientación',
        choices=Habitacion.Orientacion.choices,
        widget=forms.RadioSelect,
        error_messages={'required': 'Selecciona la orientación de la habitación.'},
    )

    class Meta:
        model = Habitacion
        fields = ['numero', 'capacidad', 'orientacion']
        widgets = {
            'numero': forms.NumberInput(
                attrs={'placeholder': 'Ej.: 101', 'autofocus': True, 'inputmode': 'numeric'}
            ),
            'capacidad': forms.NumberInput(
                attrs={'placeholder': 'Ej.: 2', 'inputmode': 'numeric'}
            ),
        }
        error_messages = {
            'numero': {
                'required': 'Ingresa el número de la habitación.',
                'min_value': 'El número debe ser mayor o igual a 1.',
            },
            'capacidad': {
                'required': 'Ingresa la capacidad de la habitación.',
                'min_value': 'La capacidad debe ser de al menos 1 pasajero.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nombre in ('numero', 'capacidad'):
            self.fields[nombre].widget.attrs.update(
                {'class': 'form-control form-control-lg', 'min': 1}
            )
