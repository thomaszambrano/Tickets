# Autor: Thomas Osorio

from django.contrib import admin
from .models import Reserva, Ticket


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'evento', 'tipo_ticket', 'cantidad', 'estado', 'fecha_reserva')
    list_filter = ('estado', 'evento')
    search_fields = ('usuario__username', 'evento__nombre')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'reserva', 'precio_final', 'usado')
    list_filter = ('usado',)
    search_fields = ('codigo',)
