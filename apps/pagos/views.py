# Author: Juan José Baron Osorio
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from apps.reservas.models import Reserva, Ticket
from .models import Pago


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
        monto = reserva.tipo_ticket.precio * reserva.cantidad

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

    monto = reserva.tipo_ticket.precio * reserva.cantidad
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

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.codigo}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    ancho, alto = A4

    # Encabezado
    p.setFont('Helvetica-Bold', 20)
    p.drawCentredString(ancho / 2, alto - 80, 'Tickets y Reservas')

    p.setFont('Helvetica', 12)
    p.drawCentredString(ancho / 2, alto - 110, 'Tu entrada para el evento')

    # Línea separadora
    p.line(50, alto - 125, ancho - 50, alto - 125)

    # Datos del ticket
    p.setFont('Helvetica-Bold', 13)
    p.drawString(60, alto - 160, f'Evento:')
    p.setFont('Helvetica', 13)
    p.drawString(160, alto - 160, ticket.reserva.evento.nombre)

    p.setFont('Helvetica-Bold', 13)
    p.drawString(60, alto - 190, f'Tipo:')
    p.setFont('Helvetica', 13)
    p.drawString(160, alto - 190, ticket.reserva.tipo_ticket.nombre)

    p.setFont('Helvetica-Bold', 13)
    p.drawString(60, alto - 220, f'Titular:')
    p.setFont('Helvetica', 13)
    p.drawString(160, alto - 220, ticket.reserva.usuario.username)

    p.setFont('Helvetica-Bold', 13)
    p.drawString(60, alto - 250, f'Precio:')
    p.setFont('Helvetica', 13)
    p.drawString(160, alto - 250, f'${ticket.precio_final}')

    p.setFont('Helvetica-Bold', 13)
    p.drawString(60, alto - 280, f'Código:')
    p.setFont('Helvetica-Bold', 13)
    p.drawString(160, alto - 280, ticket.codigo)

    # Línea separadora
    p.line(50, alto - 300, ancho - 50, alto - 300)

    p.setFont('Helvetica', 10)
    p.drawCentredString(ancho / 2, alto - 325, 'Presenta este código en la entrada del evento.')

    p.showPage()
    p.save()
    return response
