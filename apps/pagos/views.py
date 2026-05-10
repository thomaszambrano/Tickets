from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from apps.reservas.models import Reserva, Ticket

from . import services


@login_required
def pagar(request, reserva_id):
    reserva = get_object_or_404(
        Reserva.objects.select_related('evento', 'tipo_ticket', 'evento__lugar'),
        pk=reserva_id,
        usuario=request.user,
    )

    if reserva.estado != 'pendiente':
        messages.warning(request, 'Este pase no puede ser pagado.')
        return redirect('mis_reservas')

    if hasattr(reserva, 'pago') and reserva.pago.estado == 'aprobado':
        return redirect('pago_exitoso', reserva_id=reserva_id)

    monto = reserva.cantidad * reserva.tipo_ticket.precio

    if request.method == 'POST':
        metodo = request.POST.get('metodo')
        try:
            pago, _ = services.procesar_pago(
                reserva_id=reserva_id,
                metodo=metodo,
                usuario=request.user,
            )
            if reserva.usuario.email:
                send_mail(
                    f'Pase Confirmado: {reserva.evento.nombre}',
                    (
                        f'Hola {reserva.usuario.username},\n\n'
                        f'Tu pago de ${pago.monto} ha sido aprobado.\n'
                        'Ya puedes ver o descargar tu pase desde "Mis Pases".\n\n'
                        '¡Rock on!'
                    ),
                    getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@vibepas.com'),
                    [reserva.usuario.email],
                    fail_silently=True,
                )
            return redirect('pago_exitoso', reserva_id=reserva_id)
        except ValidationError as exc:
            messages.error(request, exc.message)

    return render(request, 'pagos/pagar.html', {'reserva': reserva, 'monto': monto})


@login_required
def pago_exitoso(request, reserva_id):
    reserva = get_object_or_404(
        Reserva.objects.select_related('evento', 'tipo_ticket', 'evento__lugar', 'pago'),
        pk=reserva_id,
        usuario=request.user,
    )
    return render(request, 'pagos/pago_exitoso.html', {'reserva': reserva})


@login_required
def descargar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, reserva__usuario=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.codigo}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    ancho, alto = A4

    p.setFont('Helvetica-Bold', 20)
    p.drawCentredString(ancho / 2, alto - 80, 'VibePas — Tu Entrada')
    p.setFont('Helvetica', 12)
    p.drawCentredString(ancho / 2, alto - 110, 'Presenta este código en la entrada del evento')
    p.line(50, alto - 125, ancho - 50, alto - 125)

    for label, value, y in [
        ('Evento:', ticket.reserva.evento.nombre, alto - 160),
        ('Tipo:', ticket.reserva.tipo_ticket.nombre, alto - 190),
        ('Titular:', ticket.reserva.usuario.username, alto - 220),
        ('Precio:', f'${ticket.precio_final}', alto - 250),
        ('Código:', ticket.codigo, alto - 280),
    ]:
        p.setFont('Helvetica-Bold', 13)
        p.drawString(60, y, label)
        p.setFont('Helvetica', 13)
        p.drawString(160, y, str(value))

    p.line(50, alto - 300, ancho - 50, alto - 300)
    p.showPage()
    p.save()
    return response
