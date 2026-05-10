# Autor: Thomas Osorio

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from apps.reservas.models import Reserva

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
