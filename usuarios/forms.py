from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Usuario


class RegistrarPersonalForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=120,
    )
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=150,
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
    )
    rol = forms.ChoiceField(
        label='Rol',
        choices=Usuario.Rol.choices,
        widget=forms.RadioSelect,
        initial=Usuario.Rol.RECEPCIONISTA,
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if Usuario.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Ya existe un usuario con ese nombre de usuario.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        if password:
            # Usuario temporal (sin guardar) para que los validadores
            # comparen la contraseña con el username y el nombre.
            usuario_temporal = Usuario(
                username=cleaned_data.get('username', ''),
                nombre=cleaned_data.get('nombre', ''),
            )
            try:
                validate_password(password, user=usuario_temporal)
            except forms.ValidationError as error:
                self.add_error('password', error)
        return cleaned_data

    def save(self):
        cleaned = self.cleaned_data
        return Usuario.objects.create_user(
            username=cleaned['username'],
            password=cleaned['password'],
            nombre=cleaned['nombre'],
            rol=cleaned['rol'],
        )
