from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.reservas.models import Reserva
from apps.reservas import services as reserva_services
from .models import Pago
from .email_utils import enviar_confirmacion


METODOS_VALIDOS = {'tarjeta', 'pse', 'efectivo'}


@transaction.atomic
def procesar_pago(reserva_id, metodo, usuario):
    """Create/update Pago, confirm Reserva, generate tickets. Returns (pago, tickets)."""
    if metodo not in METODOS_VALIDOS:
        raise ValidationError('Método de pago no válido.')

    reserva = get_object_or_404(
        Reserva.objects.select_related('evento', 'tipo_ticket'),
        pk=reserva_id,
        usuario=usuario,
    )

    if reserva.estado != 'pendiente':
        raise ValidationError('Este pase no puede ser pagado.')

    monto = reserva.cantidad * reserva.tipo_ticket.precio

    pago, _ = Pago.objects.get_or_create(
        reserva=reserva,
        defaults={'metodo': metodo, 'monto': monto},
    )
    pago.metodo = metodo
    pago.monto = monto
    pago.estado = 'aprobado'
    pago.save()

    reserva_services.confirmar_reserva(reserva)
    tickets = reserva_services.generar_tickets(reserva)

    enviar_confirmacion(reserva, pago)

    return pago, tickets
