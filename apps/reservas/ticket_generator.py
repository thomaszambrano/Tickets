from abc import ABC, abstractmethod
import uuid

from .models import Ticket


class TicketGenerator(ABC):
    @abstractmethod
    def generate(self, reserva) -> list:
        ...


class UUIDTicketGenerator(TicketGenerator):
    def generate(self, reserva) -> list:
        tickets = [
            Ticket(
                reserva=reserva,
                codigo=str(uuid.uuid4()),
                precio_final=reserva.tipo_ticket.precio,
            )
            for _ in range(reserva.cantidad)
        ]
        return Ticket.objects.bulk_create(tickets)


class PDFTicketGenerator(TicketGenerator):
    """Stub — future PDF+QR generation."""
    def generate(self, reserva) -> list:
        return []
