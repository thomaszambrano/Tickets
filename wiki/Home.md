# Wiki de Proyecto: Tickets y Reservas

Bienvenidos a la Wiki oficial del proyecto **Tickets y Reservas**. Esta documentación es parte de los entregables académicos y pretende proveer una vista rápida sobre la arquitectura y la evidencia de las funcionalidades requeridas en los issues asignados.

## Contenidos de la Wiki

1. **[Diagrama de Arquitectura / Clases](Arquitectura_Diagrama.md)**: Visualización estructurada usando Mermaid acerca de cómo se relacionan los modelos del dominio de la aplicación (Eventos, Lugar, Categoria, TipoTicket, Reservas).
2. **[Evidencia de Funcionalidades](Evidencia_Funcionalidades.md)**: Descripción de los avances clave que reflejan el cumplimiento de los **Issues #1 al #4**. Se incluye la re-estructuración de base de datos, implementación de datos semilla, listas paginadas, filtros y selección de ticketería.

## Referencia Rápida de Pruebas

Para validar el sistema y la funcionalidad de reservas de eventos, puede usar las siguientes credenciales insertadas desde el `seed_datos_postgres.sql`.

* **Usuario**: `cliente_demo`
* **Contraseña**: `1234`

Con este usuario, podrá iniciar sesión, consultar `/eventos/`, ver los detalles `/evento/<id>/` y hacer uso del flujo de *Reservar*. Asimismo podrá observar sus reservaciones hechas bajo en `/reservas/mis-reservas/`.
