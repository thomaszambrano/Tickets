# VibePas — Diagrama de Arquitectura

## Diagrama de Capas

```mermaid
graph TD
    subgraph Presentación ["Capa de Presentación (Views + Templates)"]
        V_EV[eventos/views.py<br/>EventoListView · EventoDetailView]
        V_RES[reservas/views.py<br/>crear_reserva · cancelar_reserva · mis_reservas]
        V_PAG[pagos/views.py<br/>pagar · pago_exitoso]
        V_USU[usuarios/views.py<br/>registro]
        TMPL[templates/<br/>base.html · catálogo · reservas · pagos]
    end

    subgraph Servicios ["Capa de Servicios (Business Logic)"]
        S_EV[eventos/services.py<br/>get_eventos_disponibles<br/>get_evento_detalle]
        S_RES[reservas/services.py<br/>crear_reserva ①<br/>cancelar_reserva ①<br/>confirmar_reserva<br/>generar_tickets]
        S_PAG[pagos/services.py<br/>procesar_pago ①]
        TG[reservas/ticket_generator.py<br/>TicketGenerator ABC<br/>UUIDTicketGenerator<br/>PDFTicketGenerator]
    end

    subgraph Dominio ["Capa de Dominio (Models)"]
        M_EV[eventos/models.py<br/>CategoriaEvento · Lugar<br/>Evento · TipoTicket]
        M_RES[reservas/models.py<br/>Reserva · Ticket]
        M_PAG[pagos/models.py<br/>Pago]
        M_USU[usuarios/models.py<br/>Perfil]
        SIG[usuarios/signals.py<br/>post_save → Perfil]
    end

    subgraph Persistencia ["Capa de Persistencia"]
        DB[(PostgreSQL 15<br/>ticketsdb)]
    end

    V_EV --> S_EV
    V_RES --> S_RES
    V_PAG --> S_PAG
    S_RES --> TG
    S_PAG --> S_RES
    S_EV --> M_EV
    S_RES --> M_RES
    S_PAG --> M_PAG
    V_USU --> M_USU
    M_USU --> SIG
    M_EV --> DB
    M_RES --> DB
    M_PAG --> DB
    M_USU --> DB
```
> ① `@transaction.atomic` + `select_for_update()` — operación atómica con bloqueo de fila

## Diagrama de Flujo — Reserva + Pago

```mermaid
sequenceDiagram
    actor U as Usuario
    participant V as View
    participant S as reservas.services
    participant P as pagos.services
    participant TG as UUIDTicketGenerator
    participant DB as PostgreSQL

    U->>V: POST /reservas/crear/<evento_id>/
    V->>S: crear_reserva(usuario, evento_id, tipo_id, cantidad)
    activate S
    S->>DB: SELECT FOR UPDATE TipoTicket
    S->>DB: UPDATE cantidad_disponible -= cantidad (F expression)
    S->>DB: INSERT Reserva
    S-->>V: Reserva (estado=pendiente)
    deactivate S

    U->>V: POST /pagos/pagar/<reserva_id>/
    V->>P: procesar_pago(reserva_id, metodo, usuario)
    activate P
    P->>DB: SELECT Reserva
    P->>DB: INSERT/UPDATE Pago (estado=aprobado)
    P->>S: confirmar_reserva(reserva)
    S->>DB: UPDATE Reserva.estado = confirmada
    P->>TG: generate(reserva)
    TG->>DB: bulk_create Ticket[]
    P-->>V: (pago, tickets)
    deactivate P
    V->>U: redirect pago_exitoso
```

## Principio de Inversión de Dependencias (DIP)

```mermaid
classDiagram
    class TicketGenerator {
        <<abstract>>
        +generate(reserva) list
    }
    class UUIDTicketGenerator {
        +generate(reserva) list
    }
    class PDFTicketGenerator {
        +generate(reserva) list
    }
    class reservas_services {
        +generar_tickets(reserva, generator)
    }

    TicketGenerator <|-- UUIDTicketGenerator
    TicketGenerator <|-- PDFTicketGenerator
    reservas_services ..> TicketGenerator : depends on interface
```

## Infraestructura Docker

```mermaid
graph LR
    subgraph Docker Compose
        WEB[web<br/>python:3.11-slim<br/>:8000]
        DB[(db<br/>postgres:15<br/>:5433)]
    end
    WEB -->|service_healthy| DB
    HOST[Host] -->|8000| WEB
    HOST -->|5433| DB
```
