from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse

def generar_pdf_ticket(ticket):
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


   
    p.setFont('Helvetica-Bold', 20)
    p.drawCentredString(ancho / 2, alto - 325, 'Presenta este código en la entrada del evento.')
    
    
    p.showPage()
    p.save()
    return response
