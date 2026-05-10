# apps/pagos

**Propósito:** Registro de pagos vinculados a reservas y descarga de tickets en PDF.

## Estado actual

Procesamiento de pagos **simulado** (todo pago se aprueba automáticamente). No hay integración con pasarela real.

## Capa de servicios (`services.py`)

`procesar_pago(reserva_id, metodo, usuario)`:
- Valida que el método sea válido (`tarjeta`, `pse`, `efectivo`)
- Verifica que la reserva esté en estado `pendiente`
- Crea o actualiza el `Pago` y lo marca como `aprobado`
- Llama a `reservas.services.confirmar_reserva()` para actualizar el estado
- Llama a `reservas.services.generar_tickets()` para crear los tickets UUID
- Todo dentro de `@transaction.atomic`

## Vistas

| Vista | URL | Descripción |
|-------|-----|-------------|
| `pagar` | `/pagos/pagar/<reserva_id>/` | Formulario de pago, delega a `services.procesar_pago` |
| `pago_exitoso` | `/pagos/exitoso/<reserva_id>/` | Confirmación post-pago |
| `descargar_ticket` | `/pagos/ticket/<ticket_id>/pdf/` | Genera y descarga PDF del ticket con reportlab |

## Modelos

`Pago` — enlace uno-a-uno con `Reserva`.
- Métodos: `tarjeta`, `pse`, `efectivo`
- Estados: `pendiente`, `aprobado`, `rechazado`

## Reglas al implementar pagos reales

Mantener el vínculo uno-a-uno `Pago ↔ Reserva`. Actualizar `Reserva.estado` tras la aprobación del pago (ya lo hace `services.confirmar_reserva`).
