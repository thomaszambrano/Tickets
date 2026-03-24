-- Datos ficticios para probar catálogo, detalle, reservación y tickets.
-- Ejecutar contra la BD: ticketsdb (PostgreSQL).
-- Nota: Diseñado para la relación 1:N Evento -> TipoTicket (FK en TipoTicket).

BEGIN;

-- 1) Categorías (3)
INSERT INTO eventos_categoriaevento (nombre, descripcion)
SELECT 'Conciertos', 'Eventos musicales en vivo'
WHERE NOT EXISTS (SELECT 1 FROM eventos_categoriaevento WHERE nombre = 'Conciertos');

INSERT INTO eventos_categoriaevento (nombre, descripcion)
SELECT 'Deportes', 'Competencias y actividades deportivas'
WHERE NOT EXISTS (SELECT 1 FROM eventos_categoriaevento WHERE nombre = 'Deportes');

INSERT INTO eventos_categoriaevento (nombre, descripcion)
SELECT 'Educacion', 'Cursos, charlas y talleres'
WHERE NOT EXISTS (SELECT 1 FROM eventos_categoriaevento WHERE nombre = 'Educacion');

-- 2) Lugares (2)
INSERT INTO eventos_lugar (nombre, direccion, ciudad, capacidad, latitud, longitud)
SELECT 'Teatro Central', 'Calle 10 #20-30', 'Medellín', 500, 6.2442, -75.5812
WHERE NOT EXISTS (
  SELECT 1 FROM eventos_lugar
  WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín'
);

INSERT INTO eventos_lugar (nombre, direccion, ciudad, capacidad, latitud, longitud)
SELECT 'Estadio Futuro', 'Av 68 #45-10', 'Bogotá', 3000, 4.71099, -74.07209
WHERE NOT EXISTS (
  SELECT 1 FROM eventos_lugar
  WHERE nombre = 'Estadio Futuro' AND ciudad = 'Bogotá'
);

-- 3) Eventos (12) para probar paginación (10 por página)
INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Concierto Rock 2026',
  'Show en vivo de rock.',
  DATE '2026-04-20',
  TIME '19:30:00',
  500,
  NULL,
  'RockCorp',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Conciertos'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Concierto Rock 2026');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Concierto Jazz 2026',
  'Noche de jazz en vivo.',
  DATE '2026-04-25',
  TIME '20:00:00',
  200,
  NULL,
  'JazzClub',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Conciertos'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Concierto Jazz 2026');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Concierto Pop 2026',
  'Tributo pop con banda invitada.',
  DATE '2026-05-01',
  TIME '18:30:00',
  450,
  NULL,
  'PopMix',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Conciertos'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Concierto Pop 2026');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Concierto Indie 2026',
  'Festival indie: música y arte.',
  DATE '2026-05-15',
  TIME '21:00:00',
  350,
  NULL,
  'IndieWay',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Conciertos'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Concierto Indie 2026');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Maratón Ciudad',
  'Carrera 10K por la ciudad.',
  DATE '2026-05-10',
  TIME '06:00:00',
  3000,
  NULL,
  'DeportesYA',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Deportes'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Estadio Futuro' AND ciudad = 'Bogotá')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Maratón Ciudad');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Copa de Fútbol 7',
  'Torneo amistoso de fútbol 7.',
  DATE '2026-06-02',
  TIME '16:00:00',
  1200,
  NULL,
  'Fut7Liga',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Deportes'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Estadio Futuro' AND ciudad = 'Bogotá')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Copa de Fútbol 7');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Ciclismo Nocturno',
  'Ruta nocturna para ciclistas.',
  DATE '2026-06-12',
  TIME '20:30:00',
  800,
  NULL,
  'CicloNocturno',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Deportes'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Estadio Futuro' AND ciudad = 'Bogotá')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Ciclismo Nocturno');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Escalada Urbana',
  'Boulder y escalada en zona urbana.',
  DATE '2026-06-20',
  TIME '09:00:00',
  500,
  NULL,
  'RocaUrbana',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Deportes'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Estadio Futuro' AND ciudad = 'Bogotá')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Escalada Urbana');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Taller Django',
  'Construye tu app con Django y buenas prácticas.',
  DATE '2026-03-30',
  TIME '09:00:00',
  120,
  NULL,
  'CodeAcademy',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Educacion'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Taller Django');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Charla DevOps',
  'CI/CD y despliegues con Docker y prácticas seguras.',
  DATE '2026-04-10',
  TIME '18:00:00',
  140,
  NULL,
  'DevOpsCol',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Educacion'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Charla DevOps');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Curso React Básico',
  'Fundamentos de React y componentes.',
  DATE '2026-04-28',
  TIME '08:30:00',
  200,
  NULL,
  'FrontendLab',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Educacion'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Curso React Básico');

INSERT INTO eventos_evento
  (nombre, descripcion, fecha, hora, capacidad, imagen, organizador, categoria_id, lugar_id)
SELECT
  'Workshop SQL',
  'Consultas avanzadas y modelado relacional.',
  DATE '2026-05-20',
  TIME '10:00:00',
  160,
  NULL,
  'DataSchool',
  (SELECT id FROM eventos_categoriaevento WHERE nombre = 'Educacion'),
  (SELECT id FROM eventos_lugar WHERE nombre = 'Teatro Central' AND ciudad = 'Medellín')
WHERE NOT EXISTS (SELECT 1 FROM eventos_evento WHERE nombre = 'Workshop SQL');

-- 4) Tipos de ticket (1:N: cada TipoTicket pertenece a un evento)
-- Concierto Rock: incluimos VIP y el General reservado para que exista relación con la taquetería.

INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'General', 50000.00, 998
FROM eventos_evento e
WHERE e.nombre = 'Concierto Rock 2026'
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'General'
  );

INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'VIP', 120000.00, 100
FROM eventos_evento e
WHERE e.nombre = 'Concierto Rock 2026'
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'VIP'
  );

-- Para el resto: solo 'General' y (en algunos casos) extra por variedad.

-- Conciertos
INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'General', 45000.00, 300
FROM eventos_evento e
WHERE e.nombre IN ('Concierto Jazz 2026', 'Concierto Pop 2026', 'Concierto Indie 2026')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'General'
  );

INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'VIP', 110000.00, 80
FROM eventos_evento e
WHERE e.nombre IN ('Concierto Jazz 2026', 'Concierto Pop 2026', 'Concierto Indie 2026')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'VIP'
  );

-- Deportes
INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'General', 60000.00, 500
FROM eventos_evento e
WHERE e.nombre IN ('Maratón Ciudad', 'Copa de Fútbol 7', 'Ciclismo Nocturno', 'Escalada Urbana')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'General'
  );

INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'VIP', 90000.00, 120
FROM eventos_evento e
WHERE e.nombre IN ('Maratón Ciudad')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'VIP'
  );

-- Educación
INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'General', 20000.00, 250
FROM eventos_evento e
WHERE e.nombre IN ('Taller Django', 'Charla DevOps', 'Curso React Básico', 'Workshop SQL')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'General'
  );

INSERT INTO eventos_tipoticket (evento_id, nombre, precio, cantidad_disponible)
SELECT e.id, 'Estudiante', 15000.00, 120
FROM eventos_evento e
WHERE e.nombre IN ('Taller Django', 'Workshop SQL')
  AND NOT EXISTS (
    SELECT 1 FROM eventos_tipoticket tt
    WHERE tt.evento_id = e.id AND tt.nombre = 'Estudiante'
  );

-- 5) Usuario demo (para que exista reserva y ticket)
INSERT INTO auth_user
  (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
SELECT
  'pbkdf2_sha256$600000$N74TW4xjCDxA1gnBca6UO1$C1OAPKuYp0DbQp9UI7jbv0ytgJoPIwUVo+N3WMNz1LM=',
  NULL, FALSE,
  'cliente_demo', 'Demo', 'Cliente', 'cliente_demo@example.com',
  FALSE, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM auth_user WHERE username = 'cliente_demo');

INSERT INTO usuarios_perfil (telefono, documento, user_id)
SELECT '', '', u.id
FROM auth_user u
WHERE u.username = 'cliente_demo'
  AND NOT EXISTS (SELECT 1 FROM usuarios_perfil p WHERE p.user_id = u.id);

-- 6) Reserva demo + Ticket (relación con taquetería)
-- Reservamos 2 'General' del evento 'Concierto Rock 2026'
WITH u AS (
  SELECT id FROM auth_user WHERE username = 'cliente_demo'
),
e AS (
  SELECT id FROM eventos_evento WHERE nombre = 'Concierto Rock 2026'
),
t AS (
  SELECT id, evento_id, nombre FROM eventos_tipoticket
  WHERE nombre = 'General' AND evento_id = (SELECT id FROM e)
),
ins_reserva AS (
  INSERT INTO reservas_reserva (usuario_id, evento_id, tipo_ticket_id, cantidad, fecha_reserva, estado)
  SELECT u.id, e.id, t.id, 2, NOW(), 'pendiente'
  FROM u, e, t
  WHERE NOT EXISTS (
    SELECT 1 FROM reservas_reserva r
    WHERE r.usuario_id = u.id
      AND r.evento_id = e.id
      AND r.tipo_ticket_id = t.id
  )
  RETURNING id
)
INSERT INTO reservas_ticket (reserva_id, codigo, precio_final, usado)
SELECT
  ins_reserva.id,
  'TCK-DEMO-0001',
  100000.00,
  FALSE
FROM ins_reserva
WHERE NOT EXISTS (
  SELECT 1 FROM reservas_ticket tk WHERE tk.codigo = 'TCK-DEMO-0001'
);

COMMIT;

