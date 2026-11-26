from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nombre', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    fieldsets = UserAdmin.fieldsets + (('Hotel El Aura', {'fields': ('nombre', 'rol')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Hotel El Aura', {'fields': ('nombre', 'rol')}),
    )
