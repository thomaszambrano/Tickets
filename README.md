# 🎟️ Tickets y Reservas

Sistema web de gestión de eventos, reservas y pagos de tickets desarrollado con **Django 4.2** y **PostgreSQL**, desplegado con **Docker Compose**.

## 📋 Tabla de contenidos
- [Descripción general](#descripción-general)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelos del dominio](#modelos-del-dominio)
- [Rutas disponibles](#rutas-disponibles)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Variables de entorno](#variables-de-entorno)
- [Flujo de autenticación](#flujo-de-autenticación)
- [Panel de administración](#panel-de-administración)
- [Autor](#autor)

---

## Descripción general
La aplicación permite a usuarios finales explorar eventos disponibles, realizar reservas de tickets y consultar el historial de sus reservas. Los administradores gestionan toda la información desde un panel dedicado separado de la vista del usuario final.

Las dos secciones principales son:
1. **Sección pública / usuario final** — exploración de eventos, detalle de evento, creación y cancelación de reservas.
2. **Sección de administración** — gestión completa de eventos, lugares, categorías, tickets, reservas y pagos desde `/admin/`.

---

## Tecnologías utilizadas

| Tecnología | Versión | Rol |
| :--- | :--- | :--- |
| **Python** | 3.11 | Lenguaje base |
| **Django** | 4.2.29 | Framework web |
| **PostgreSQL** | 15 | Base de datos relacional |
| **psycopg2-binary** | 2.9.11 | Adaptador PostgreSQL para Django |
| **Pillow** | 10.4.0 | Manejo de imágenes (campo ImageField) |
| **Docker / Docker Compose** | — | Contenedores y orquestación |

---

## Estructura del proyecto

```text
Tickets/
├── config/                  # Configuración central del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── usuarios/            # Perfil extendido del usuario
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── signals.py       # Auto-creación de Perfil al registrar User
│   │   └── apps.py
│   ├── eventos/             # Eventos, lugares, categorías y tipos de ticket
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── reservas/            # Reservas y tickets generados
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── admin.py
│   └── pagos/               # Registro de pagos asociados a reservas
│       ├── models.py
│       ├── admin.py
│       └── urls.py
├── templates/
│   ├── base.html            # Plantilla base con navbar y mensajes
│   ├── auth/
│   │   └── login.html
│   ├── eventos/
│   │   ├── home.html
│   │   └── detalle_evento.html
│   └── reservas/
│       ├── mis_reservas.html
│       └── crear_reserva.html
├── dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## Modelos del dominio

### `apps.usuarios`
| Modelo | Campos principales |
| :--- | :--- |
| **Perfil** | `user` (OneToOne → User), `telefono`, `documento` |
> [!NOTE]
> El Perfil se crea automáticamente vía señal `post_save` cada vez que se registra un nuevo `User`.

### `apps.eventos`
| Modelo | Campos principales |
| :--- | :--- |
| **CategoriaEvento** | `nombre`, `descripcion` |
| **Lugar** | `nombre`, `direccion`, `ciudad`, `capacidad` |
| **Evento** | `nombre`, `descripcion`, `fecha`, `hora`, `capacidad_total`, `imagen`, `categoria` (FK), `lugar` (FK) |
| **TipoTicket** | `evento` (FK), `nombre`, `precio`, `cantidad_disponible` |

### `apps.reservas`
| Modelo | Campos principales |
| :--- | :--- |
| **Reserva** | `usuario` (FK → User), `evento` (FK), `tipo_ticket` (FK), `cantidad`, `fecha_reserva`, `estado` |
| **Ticket** | `reserva` (FK), `codigo`, `precio_final`, `usado` |
*   **Estados de Reserva:** `pendiente` · `confirmada` · `cancelada`

### `apps.pagos`
| Modelo | Campos principales |
| :--- | :--- |
| **Pago** | `reserva` (OneToOne), `metodo`, `monto`, `estado`, `referencia`, `fecha_pago` |
*   **Métodos de pago:** `tarjeta` · `pse` · `efectivo`
*   **Estados de pago:** `pendiente` · `aprobado` · `rechazado`

---

## Rutas disponibles

| Método | URL | Nombre | Acceso | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| GET | `/` | `home` | Público | Lista de eventos disponibles |
| GET | `/evento/<id>/` | `detalle_evento` | Público | Detalle de un evento y sus tipos de ticket |
| GET/POST | `/accounts/login/` | `login` | Público | Formulario de inicio de sesión |
| POST | `/accounts/logout/` | `logout` | Autenticado | Cierra sesión y redirige a home |
| GET | `/reservas/mis-reservas/` | `mis_reservas` | Autenticado | Lista de reservas del usuario |
| GET/POST | `/reservas/crear/<evento_id>/` | `crear_reserva` | Autenticado | Formulario para crear una reserva |
| POST | `/reservas/cancelar/<reserva_id>/` | `cancelar_reserva` | Autenticado | Cancela una reserva pendiente |
| GET | `/admin/` | — | Staff | Panel de administración |

---

## Instalación y ejecución

### Requisitos previos
*   Docker y Docker Compose instalados.

### Pasos
1.  **Clonar el repositorio**
    ```bash
    git clone <url-del-repositorio>
    cd Tickets
    ```
2.  **Levantar los contenedores**
    ```bash
    docker compose up --build
    ```
3.  **Aplicar migraciones**
    ```bash
    docker compose exec web python manage.py migrate
    ```
4.  **Crear superusuario**
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```
5.  **Acceder a la aplicación**
    | URL | Descripción |
    | :--- | :--- |
    | http://localhost:8000/ | Aplicación principal |
    | http://localhost:8000/admin/ | Panel de administración |

---

## Variables de entorno
Configuradas en `docker-compose.yml`. Para entornos distintos a desarrollo, se recomienda usar un archivo `.env`.

| Variable | Valor por defecto | Descripción |
| :--- | :--- | :--- |
| **DB_NAME** | `ticketsdb` | Nombre de la base de datos |
| **DB_USER** | `postgres` | Usuario de PostgreSQL |
| **DB_PASSWORD** | `postgres` | Contraseña de PostgreSQL |
| **DB_HOST** | `db` | Host del servicio de base de datos |
| **DB_PORT** | `5432` | Puerto de PostgreSQL |

> [!WARNING]
> En producción reemplaza `SECRET_KEY` in `settings.py` por una clave segura y establece `DEBUG = False`.

---

## Flujo de autenticación

**Usuario no autenticado**
- `/accounts/login/` ──► credenciales válidas ──► redirige a `/` (home)
- Vista protegida ──► redirige automáticamente a login (`LOGIN_URL = 'login'`)

**Usuario autenticado**
- Puede ver: `home`, `detalle de evento`
- Puede usar: `mis reservas`, `crear reserva`, `cancelar reserva`
- `POST /accounts/logout/` ──► redirige a `/` (home)

Las vistas privadas usan el decorador `@login_required`. Si un usuario no autenticado intenta acceder, Django lo redirige a `/accounts/login/` automáticamente.

---

## Panel de administración
Accesible en `/admin/` únicamente para usuarios con `is_staff = True`.

| Modelo | Buscar por | Filtrar por |
| :--- | :--- | :--- |
| **Evento** | `nombre` | `categoría`, `fecha` |
| **TipoTicket** | — | `evento` |
| **Lugar** | `nombre`, `ciudad` | — |
| **CategoriaEvento** | `nombre` | — |
| **Reserva** | `usuario`, `evento` | `estado`, `evento` |
| **Ticket** | `código` | `usado` |
| **Pago** | `referencia` | `estado`, `método` |
| **Perfil** | `usuario`, `documento` | — |

---

## Autores
**Thomas Osorio**
**Juan Jose Baron**
**Emmanuel Hernandez**
Proyecto académico — Sistema de Tickets y Reservas
Django 4.2 · PostgreSQL 15 · Docker
