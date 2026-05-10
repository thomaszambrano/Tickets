# apps/reservas

**Propósito:** Flujo de reservas — selección de entradas, gestión de disponibilidad, cancelación y generación de tickets.

## Invariantes críticos

- `ReservaForm` **siempre** necesita el kwarg `evento=<instancia_evento>` — restringe el queryset de `TipoTicket` al evento correspondiente. Omitirlo causa opciones incorrectas o errores 500.
- La disponibilidad (`TipoTicket.cantidad_disponible`) se decrementa al reservar y se restaura al cancelar **dentro de `services.py`** con `@transaction.atomic` + `select_for_update()`. Nunca hacer esto directamente en las vistas.
- La cancelación solo se permite cuando `reserva.estado == 'pendiente'`. `services.cancelar_reserva` ya hace esta verificación.
- Todas las vistas usan `@login_required` — nunca quitar ese decorador.

## Máquina de estados

```
pendiente → cancelada     (usuario cancela, se restaura disponibilidad)
pendiente → confirmada    (pago aprobado vía apps.pagos.services)
```

## Capa de servicios (`services.py`)

| Función | Descripción |
|---------|-------------|
| `crear_reserva(usuario, evento_id, tipo_ticket_id, cantidad)` | Atómica: decrementa stock y crea Reserva |
| `cancelar_reserva(reserva_id, usuario)` | Atómica: restaura stock y cambia estado |
| `confirmar_reserva(reserva)` | Cambia estado a `confirmada` (llamado por pagos) |
| `generar_tickets(reserva, generator=None)` | Genera Ticket[] vía TicketGenerator |

## DIP — Generación de tickets (`ticket_generator.py`)

- `TicketGenerator` — clase abstracta (ABC)
- `UUIDTicketGenerator` — implementación de producción, genera códigos UUID completos con `bulk_create`
- `PDFTicketGenerator` — stub para futura implementación

## Archivos

- `services.py` — toda la lógica de negocio
- `ticket_generator.py` — jerarquía DIP para generación de tickets
- `forms.py` — ReservaForm con filtrado dinámico de TipoTicket
- `models.py` — Reserva (tiene `estado` + `clean()`), Ticket
- `tests.py` — 6 tests unitarios de lógica de negocio
