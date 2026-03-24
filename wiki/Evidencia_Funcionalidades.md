# Evidencia de Funcionalidades Interesantes

En esta sección se detallan las implementaciones sobresalientes desarrolladas correspondientes a los Issues asignados referidos al Módulo: **Catálogo de Eventos**.

## 1. Migración y Evolución del Modelo de Datos (Issues #1 y #4)
Se modeló eficientemente el catálogo de manera que fuese extensible e integrable:
* **Entidades Relacionadas Extensibles**: Se configuraron las dependencias correctas para `Evento`, extendiéndolo con las ForeignKey respectivas de `CategoriaEvento` y `Lugar`. 
* **Atributos Clave Añadidos**: `Lugar` fue dotado de geocodificación (`latitud` y `longitud`), sumamente útil para un proyecto de boletería moderna.  `Evento` incorporó `capacidad` y `organizador`.  `TipoTicket` fue validado sistemáticamente para acoplarse 1:N con `Evento`.
* **Seguridad en Formularios (Form validation)**: Se mejoró `ReservaForm` para que la capa de validación en Django detecte e invalide intenciones de manipular POST requests en donde se intente inyectar un ID de `TipoTicket` que no pertenezca al evento visualizado.

## 2. Paginación y Filtrado Dinámico (Issue #2)
La ruta `/eventos/` fue conectada a una vista de base genérica de Django `ListView` (`EventoListView`) dotada con características avanzadas:
* **Filtros Manuales Eficientes**: Evitando agregar dependencias masivas por defecto, se implementó el filtrado a través del método `get_queryset()` interceptando los parámetros GET de búsqueda por palabra clave (`q`), Rango de Fechas (`fecha_inicio`, `fecha_fin`) e ID de `categoria`.
* **Paginación Consistente**: Paginación en bloques (10 eventos max). Para no dañar la usabilidad en búsquedas compuestas, el objeto del `Paginator` fue entrelazado con una función que conserva los Query Params vigentes de los filtros durante la navegación por los controles de páginas.

## 3. UI Dinámica y Formularios de Reserva (Issue #3)
El proyecto avanzó a utilizar Bootstrap de manera transversal, logrando vistas orientadas a una experiencia superior para la venta.
* El detalle del Evento `/evento/<id>/` no solamente enumera en texto plano lo que hay, sino que inserta una tabla enriquecida. 
* Los botones por fila de ticket están conectados, vía parámetros GET, con el formulario transaccional `/reservas/crear/<id_evento>/?tipo=<id_ticket>` que hace una pre-selección automática facilitando la tarea al usuario y evitando equivocaciones.

## 4. Datos de Prueba (Seed SQL)
Para enriquecer la fase de pruebas, se construyó el script `seed_datos_postgres.sql`. Sus características más interesantes son:
* Emplea condicionales tipo `WHERE NOT EXISTS` en sus inserts para asegurar que pueda correrse de manera **idempotente** (segura, varias veces sin romper la DB con errores de Unique Constraint).
* Cuenta con hashes pre-calculados al estilo de `auth_user` de Django (PBKDF2), permitiendo precargar exitosamente al usuario _"cliente_demo"_ cuya contraseña operativa es `1234`.
