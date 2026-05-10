from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from apps.eventos.models import TipoTicket
from .models import Reserva
from .ticket_generator import UUIDTicketGenerator


_generator = UUIDTicketGenerator()


@transaction.atomic
def crear_reserva(usuario, evento_id, tipo_ticket_id, cantidad):
    """Decrement availability atomically; raise ValidationError if stock is insufficient."""
    tipo = TipoTicket.objects.select_for_update().get(
        pk=tipo_ticket_id, evento_id=evento_id
    )
    if cantidad > tipo.cantidad_disponible:
        raise ValidationError(
            f'Solo hay {tipo.cantidad_disponible} pases disponibles.'
        )
    TipoTicket.objects.filter(pk=tipo.pk).update(
        cantidad_disponible=F('cantidad_disponible') - cantidad
    )
    reserva = Reserva.objects.create(
        usuario=usuario,
        evento_id=evento_id,
        tipo_ticket=tipo,
        cantidad=cantidad,
    )
    return reserva


@transaction.atomic
def cancelar_reserva(reserva_id, usuario):
    """Restore availability atomically; raise ValidationError if not cancellable."""
    reserva = get_object_or_404(
        Reserva.objects.select_for_update().select_related('tipo_ticket'),
        pk=reserva_id,
        usuario=usuario,
    )
    if reserva.estado != 'pendiente':
        raise ValidationError('Solo se pueden cancelar pases en estado pendiente.')
    TipoTicket.objects.filter(pk=reserva.tipo_ticket_id).update(
        cantidad_disponible=F('cantidad_disponible') + reserva.cantidad
    )
    reserva.estado = 'cancelada'
    reserva.save(update_fields=['estado'])
    return reserva


def confirmar_reserva(reserva):
    """Mark a reservation as confirmed (called after payment approval)."""
    reserva.estado = 'confirmada'
    reserva.save(update_fields=['estado'])
    return reserva


def generar_tickets(reserva, generator=None):
    gen = generator or _generator
    return gen.generate(reserva)
