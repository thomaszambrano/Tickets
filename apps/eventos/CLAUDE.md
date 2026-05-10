# apps/eventos

**Propósito:** Catálogo central de eventos — categorías, lugares, eventos y tipos de entrada.

## Comportamientos clave

- `EventoListView` filtra mediante parámetros GET: `categoria`, `fecha_inicio`, `fecha_fin`, `nombre`. Siempre preservar estos parámetros al paginar (patrón `?page=N&categoria=X`).
- `TipoTicket.cantidad_disponible` es el contador oficial de stock. Solo `apps.reservas.services` debe modificarlo.
- `Evento.capacidad` y `Evento.organizador` tienen valores por defecto en el modelo, pero los valores reales vienen del seed SQL — no confiar en los defaults en los tests.

## Capa de servicios

`apps/eventos/services.py` expone:
- `get_eventos_disponibles(categoria, fecha_inicio, fecha_fin, nombre)` — consulta con `select_related` y `prefetch_related`
- `get_evento_detalle(evento_id)` — carga el evento con todos los tipos de ticket relacionados

Las vistas delegan a estos servicios; no hacer consultas directas al ORM desde las vistas.

## Modelos

- `CategoriaEvento` → `Evento` → `TipoTicket` (un evento, muchos tipos de entrada)
- `Lugar` — recinto, FK en `Evento`
