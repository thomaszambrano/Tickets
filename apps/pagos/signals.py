# Author: Juan José Baron Osorio
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pago
from apps.reservas.models import Ticket


def _codigo_unico():
    return str(uuid.uuid4()).replace('-', '').upper()[:20]


@receiver(post_save, sender=Pago)
def confirmar_reserva_y_generar_tickets(sender, instance, created, **kwargs):
    if instance.estado != 'aprobado':
        return

    reserva = instance.reserva

    if reserva.estado != 'confirmada':
        reserva.estado = 'confirmada'
        reserva.save(update_fields=['estado'])

    if not reserva.tickets.exists():
        precio_unitario = reserva.tipo_ticket.precio
        tickets = [
            Ticket(
                reserva=reserva,
                precio_final=precio_unitario,
                codigo=_codigo_unico(),
            )
            for _ in range(reserva.cantidad)
        ]
        Ticket.objects.bulk_create(tickets)