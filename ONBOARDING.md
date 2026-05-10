# VibePas — Onboarding Guide

> New to the project? Start here. You'll be running it locally in under 10 minutes.

## What is VibePas?

A Django 4.2 web app for event management, ticket reservations, and payments. Built for a university project with PostgreSQL 15 and Docker Compose.

## Project state (as of May 2026)

### Done ✅
| Feature | Location |
|---------|----------|
| Event catalog with filters (category, date, name) | `apps/eventos/` |
| Reservation flow with atomic stock decrement | `apps/reservas/services.py` |
| Payment processing (simulated) | `apps/pagos/services.py` |
| Ticket generation via DIP (TicketGenerator ABC) | `apps/reservas/ticket_generator.py` |
| User registration + login | `apps/usuarios/` |
| i18n: Spanish + English language switcher | `locale/`, `templates/partials/language_switcher.html` |
| 6 unit tests | `apps/reservas/tests.py` |
| Architecture documentation (Mermaid) | `docs/ARCHITECTURE.md` |
| Docker Compose with healthchecks | `docker-compose.yml` |

### Pending ❌ (GitHub Issues open)
| Feature | Issue |
|---------|-------|
| Cloud deployment (Railway/Render) | #1 |
| Compile .mo files for i18n | #2 |
| QR ticket generation | #3 |
| Custom 404/500 pages | #4 |
| Email confirmations (SMTP) | #5 |
| 80%+ test coverage | #7 |
| SEO + robots.txt | #8 |

## Architecture overview

```
Browser → Django Views → Services (business logic) → Models → PostgreSQL
                    ↓
            TicketGenerator (ABC)
            ├── UUIDTicketGenerator (production)
            └── PDFTicketGenerator (stub / future)
```

Key design: **no business logic in views**. Views only handle HTTP (forms, messages, redirects). All business rules live in `services.py` files.

See `docs/ARCHITECTURE.md` for full Mermaid diagrams.

## Quick start (local)

**Prerequisites:** Docker Desktop running.

```bash
# 1. Clone
git clone https://github.com/thomaszambrano/Tickets
cd Tickets

# 2. Copy env file
cp .env.example .env
# Edit .env if needed (defaults work for local Docker)

# 3. Start containers
docker compose up --build -d

# 4. Apply migrations
docker compose exec web python manage.py migrate

# 5. Load seed data (categories, venues, events, demo user)
docker compose exec -T db psql -U postgres -d ticketsdb < seed_datos_postgres.sql

# 6. Compile translations
docker compose exec web python manage.py compilemessages

# 7. Open the app
open http://localhost:8000
```

**Demo user:** `demo@vibepas.co` / `demo1234` (from seed data)

**Admin panel:** http://localhost:8000/admin — create a superuser first:
```bash
docker compose exec web python manage.py createsuperuser
```

## Running tests

```bash
docker compose exec web python manage.py test
```

## Key files

| File | Purpose |
|------|---------|
| `apps/reservas/services.py` | Reservation business logic (atomic) |
| `apps/pagos/services.py` | Payment processing |
| `apps/reservas/ticket_generator.py` | DIP ticket generation |
| `apps/reservas/tests.py` | Unit tests |
| `config/settings.py` | Django settings (env-driven) |
| `docker-compose.yml` | Local infrastructure |
| `.env.example` | Required environment variables |
| `docs/ARCHITECTURE.md` | System architecture diagrams |
| `seed_datos_postgres.sql` | Demo data |

## Git workflow

```bash
git checkout -b feat/your-feature
# work...
git commit -m "feat: description"
git push origin feat/your-feature
# open PR against main
```

Branch naming: `feat/`, `fix/`, `chore/`, `docs/`

## Troubleshooting

**Port 5432 conflict:** PostgreSQL is exposed on **5433**, not 5432. If you have a local PG instance, make sure it's not on 5433.

**Migrations out of sync:** `docker compose exec web python manage.py migrate`

**Language switcher not working:** Run `compilemessages` (see step 6 above).

**Container not starting:** `docker compose logs web` to see errors.
