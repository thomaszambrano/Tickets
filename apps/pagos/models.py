# Autor: Thomas Osorio

from django.db import models
from apps.reservas.models import Reserva

class Pago(models.Model):
    METODOS = [
        ('tarjeta', 'Tarjeta'),
        ('pse', 'PSE'),
        ('efectivo', 'Efectivo'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='pago')
    metodo = models.CharField(max_length=20, choices=METODOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    referencia = models.CharField(max_length=100, blank=True)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago #{self.id} - {self.estado}"