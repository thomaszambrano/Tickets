# Autor: Thomas Osorio

from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'documento')
    search_fields = ('user__username', 'documento')
