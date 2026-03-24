# Diagrama de Clases y Arquitectura

Adicional a la documentación técnica general, en esta página se modela de manera gráfica las relaciones implementadas entre los principales componentes del sistema, incluyendo los modelos ajustados bajo el flujo 1:N que corresponde a las reglas particulares del proyecto (Un `TipoTicket` pertenece invariablemente a un único evento).

## Modelos de Base de Datos - Diagrama ER/Clases

```mermaid
classDiagram
    direction TB
    
    class User {
        +String username
        +String password
        +String email
        +Boolean is_active
    }
    class Perfil {
        +String telefono
        +String documento
    }
    class CategoriaEvento {
        +String nombre
        +String descripcion
    }
    class Lugar {
        +String nombre
        +String ciudad
        +String direccion
        +Integer capacidad
        +Float latitud
        +Float longitud
    }
    class Evento {
        +String nombre
        +Date fecha
        +Time hora
        +Integer capacidad
        +String organizador
        +String descripcion
    }
    class TipoTicket {
        +String nombre
        +Decimal precio
        +Integer cantidad_disponible
    }
    class Reserva {
        +Integer cantidad
        +DateTime fecha_reserva
        +String estado
    }
    class Ticket {
        +String codigo
        +Decimal precio_final
        +Boolean usado
    }

    User "1" -- "1" Perfil : tiene
    CategoriaEvento "1" -- "*" Evento : clasifica
    Lugar "1" -- "*" Evento : alberga
    Evento "1" -- "*" TipoTicket : dispone de
    Evento "1" -- "*" Reserva : recibe
    User "1" -- "*" Reserva : realiza
    TipoTicket "1" -- "*" Reserva : referenciado por
    Reserva "1" -- "*" Ticket : genera
```

### Notas sobre la Arquitectura

1. **Relación Evento-TipoTicket**: Se confirmó que de cara al modelo de negocio de este proyecto particular, se gestiona una relación **1:N** (ForeingKey en TipoTicket que apunta a Evento) y no una M2M (ManyToMany), esto para garantizar que un ticket (ej. General) pertenezca e impacte la cantidad disponible de un solo evento específico y no cruce la contabilidad de entradas si existen solapamientos de ventas.
2. **Latitud y Longitud en Lugar**: En cumplimiento con los requisitos de enriquecer el modelo del Catálogo, la entidad `Lugar` posee latitud y longitud, abriendo así las puertas a la visualización de Mapas en futuras integraciones.
3. **Flujo de Reservas**: La entidad intermedia abstracta de `Reserva` es la encargada de descontar del volumen disponible de un `TipoTicket` y, al ser confirmadas o pagadas, permite desencadenar de forma explícita la creación serializada en `Ticket`.
