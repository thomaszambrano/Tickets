from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.eventos.models import CategoriaEvento, Evento, Lugar, TipoTicket
from apps.reservas import services
from apps.reservas.models import Reserva, Ticket
from apps.reservas.ticket_generator import UUIDTicketGenerator


def _make_base_data():
    categoria = CategoriaEvento.objects.create(nombre='Rock')
    lugar = Lugar.objects.create(
        nombre='Coliseo', direccion='Cra 1', ciudad='Bogotá', capacidad=5000
    )
    evento = Evento.objects.create(
        nombre='Festival Test',
        descripcion='desc',
        fecha='2026-12-01',
        hora='20:00',
        capacidad=500,
        organizador='Org',
        categoria=categoria,
        lugar=lugar,
    )
    return evento


class CrearReservaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('tester', password='pass')
        self.evento = _make_base_data()
        self.tipo = TipoTicket.objects.create(
            evento=self.evento, nombre='General', precio=50000, cantidad_disponible=100
        )

    def test_reserva_descuenta_cantidad_disponible(self):
        services.crear_reserva(self.usuario, self.evento.id, self.tipo.id, 5)
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.cantidad_disponible, 95)

    def test_no_se_puede_reservar_mas_de_lo_disponible(self):
        tipo_escaso = TipoTicket.objects.create(
            evento=self.evento, nombre='VIP', precio=100000, cantidad_disponible=2
        )
        with self.assertRaises(ValidationError):
            services.crear_reserva(self.usuario, self.evento.id, tipo_escaso.id, 5)
        tipo_escaso.refresh_from_db()
        self.assertEqual(tipo_escaso.cantidad_disponible, 2)  # no se modificó

    def test_cancelar_reserva_restaura_disponibilidad(self):
        reserva = services.crear_reserva(self.usuario, self.evento.id, self.tipo.id, 3)
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.cantidad_disponible, 97)

        services.cancelar_reserva(reserva.id, self.usuario)
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.cantidad_disponible, 100)

        reserva.refresh_from_db()
        self.assertEqual(reserva.estado, 'cancelada')

    def test_ticket_codigo_es_unico(self):
        reserva1 = services.crear_reserva(self.usuario, self.evento.id, self.tipo.id, 1)
        reserva2 = services.crear_reserva(self.usuario, self.evento.id, self.tipo.id, 1)

        gen = UUIDTicketGenerator()
        tickets1 = gen.generate(reserva1)
        tickets2 = gen.generate(reserva2)

        codigos = {t.codigo for t in tickets1} | {t.codigo for t in tickets2}
        self.assertEqual(len(codigos), 2)


class ReservaModelCleanTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('tester2', password='pass')
        self.evento = _make_base_data()
        self.tipo = TipoTicket.objects.create(
            evento=self.evento, nombre='General', precio=30000, cantidad_disponible=10
        )

    def test_clean_raises_when_cantidad_exceeds_disponible(self):
        reserva = Reserva(
            usuario=self.usuario,
            evento=self.evento,
            tipo_ticket=self.tipo,
            cantidad=50,
        )
        with self.assertRaises(ValidationError):
            reserva.clean()

    def test_clean_passes_when_cantidad_ok(self):
        reserva = Reserva(
            usuario=self.usuario,
            evento=self.evento,
            tipo_ticket=self.tipo,
            cantidad=5,
        )
        reserva.clean()  # no exception
