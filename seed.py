import os
from datetime import date, time
from django.contrib.auth.models import User
from apps.eventos.models import CategoriaEvento, Lugar, Evento, TipoTicket
from apps.usuarios.models import Perfil

def run():
    cat_c, _ = CategoriaEvento.objects.get_or_create(nombre='Conciertos', defaults={'descripcion': 'Eventos musicales'})
    cat_d, _ = CategoriaEvento.objects.get_or_create(nombre='Deportes', defaults={'descripcion': 'Competencias'})
    cat_e, _ = CategoriaEvento.objects.get_or_create(nombre='Educacion', defaults={'descripcion': 'Cursos'})
    
    lugar_m, _ = Lugar.objects.get_or_create(nombre='Teatro Central', ciudad='Medellín', defaults={'direccion': 'Calle 10', 'capacidad': 500})
    lugar_b, _ = Lugar.objects.get_or_create(nombre='Estadio Futuro', ciudad='Bogotá', defaults={'direccion': 'Av 68', 'capacidad': 3000})
    
    evento1, _ = Evento.objects.get_or_create(nombre='Concierto Rock 2026', defaults={'descripcion': 'Rock', 'fecha': date(2026,4,20), 'hora': time(19,30), 'capacidad': 500, 'categoria': cat_c, 'lugar': lugar_m})
    if _:
        TipoTicket.objects.create(evento=evento1, nombre='General', precio=50000, cantidad_disponible=998)
        TipoTicket.objects.create(evento=evento1, nombre='VIP', precio=120000, cantidad_disponible=100)

    evento_maraton, _ = Evento.objects.get_or_create(nombre='Maratón Ciudad', defaults={'descripcion': '10K', 'fecha': date(2026,5,10), 'hora': time(6,0), 'capacidad': 3000, 'categoria': cat_d, 'lugar': lugar_b})
    if _:
        TipoTicket.objects.create(evento=evento_maraton, nombre='General', precio=60000, cantidad_disponible=500)
    
    user, created = User.objects.get_or_create(username='cliente_demo', defaults={'is_active': True, 'email': 'demo@example.com'})
    if created:
        user.set_password('cliente_demo')
        user.save()
    
    # Test F1: check if Perfil was created by signals
    perfil_exists = Perfil.objects.filter(user=user).exists()
    print('TEST F1 - Perfil auto-created:', perfil_exists)
    
    print('Seed complete!')
