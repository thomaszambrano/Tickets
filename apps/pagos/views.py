# Author: Juan José Baron Osorio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from apps.reservas.models import Reserva, Ticket
from .models import Pago
from .utils import generar_pdf_ticket


@login_required
def crear_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario=request.user)

    # Evitar pagar una reserva ya confirmada o cancelada
    if reserva.estado != 'pendiente':
        messages.warning(request, 'Esta reserva no puede ser pagada.')
        return redirect('mis_reservas')

    # Evitar crear un pago duplicado
    if hasattr(reserva, 'pago') and reserva.pago.estado == 'aprobado':
        messages.info(request, 'Esta reserva ya fue pagada.')
        return redirect('mis_reservas')

    if request.method == 'POST':
        metodo = request.POST.get('metodo')
        monto = reserva.calcular_total()

        pago, created = Pago.objects.get_or_create(
            reserva=reserva,
            defaults={
                'metodo': metodo,
                'monto': monto,
                'estado': 'pendiente',
            }
        )

        # Si ya existía, actualizamos el método
        if not created:
            pago.metodo = metodo
            pago.monto = monto

        # Simulación: todo pago se aprueba automáticamente
        pago.estado = 'aprobado'
        pago.save()

        messages.success(request, '¡Pago realizado exitosamente!')
        return redirect('mis_reservas')

    monto = reserva.calcular_total()
    return render(request, 'pagos/pago.html', {
        'reserva': reserva,
        'monto': monto,
    })

@login_required
def descargar_ticket(request, ticket_id):
    ticket = get_object_or_404(
        Ticket,
        pk=ticket_id,
        reserva__usuario=request.user
    )

    # Delegamos toda la lógica gráfica del ticket a nuestra utilidad
    return generar_pdf_ticket(ticket)
