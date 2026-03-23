# Autor: Thomas Osorio

from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'metodo', 'monto', 'estado', 'fecha_pago')
    list_filter = ('estado', 'metodo')
    search_fields = ('referencia',)
