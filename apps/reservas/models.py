# Autor: Thomas Osorio

from django.db import models
from django.contrib.auth.models import User
from apps.eventos.models import Evento, TipoTicket

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='reservas')
    tipo_ticket = models.ForeignKey(TipoTicket, on_delete=models.CASCADE, related_name='reservas')
    cantidad = models.PositiveIntegerField()
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.username}"


class Ticket(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='tickets')
    codigo = models.CharField(max_length=100, unique=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    usado = models.BooleanField(default=False)

    def __str__(self):
        return self.codigo