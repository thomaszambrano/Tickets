# Autor: Thomas Osorio

from django.contrib import admin
from .models import CategoriaEvento, Evento, Lugar, TipoTicket


@admin.register(CategoriaEvento)
class CategoriaEventoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'capacidad')
    search_fields = ('nombre', 'ciudad')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'lugar', 'categoria', 'capacidad', 'organizador')
    list_filter = ('categoria', 'fecha')
    search_fields = ('nombre',)


@admin.register(TipoTicket)
class TipoTicketAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'precio', 'cantidad_disponible')
    list_filter = ('evento',)
    search_fields = ('nombre',)
