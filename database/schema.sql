CREATE DATABASE IF NOT EXISTS noreste_grill;
USE noreste_grill;

CREATE TABLE Rol (
    id_rol VARCHAR(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    CONSTRAINT pk_rol PRIMARY KEY (id_rol)
);

CREATE TABLE Usuarios (
    no_empleado INT NOT NULL,
    id_rol VARCHAR(10) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    ultimo_acceso DATETIME NULL,
    CONSTRAINT pk_usuarios PRIMARY KEY (no_empleado),
    UNIQUE (correo),
    UNIQUE (nombre_usuario),
    CONSTRAINT fk_usuarios_rol
        FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE Mesa (
    id_mesa INT NOT NULL,
    no_empleado INT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'libre',
    nombre_cliente VARCHAR(80) NULL,
    no_personas INT NULL,
    hora_inicio DATETIME NULL,
    razon_retraso VARCHAR(100) NULL,
    comentario_retraso VARCHAR(255) NULL,
    CONSTRAINT pk_mesa PRIMARY KEY (id_mesa),
    CONSTRAINT fk_mesa_usuarios
        FOREIGN KEY (no_empleado) REFERENCES Usuarios(no_empleado)
);

CREATE TABLE Reservacion (
    id_reservacion INT NOT NULL AUTO_INCREMENT,
    no_empleado INT NOT NULL,
    nombre_cliente VARCHAR(50) NOT NULL,
    apellido_cliente VARCHAR(50) NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    no_personas INT NOT NULL,
    estado VARCHAR(20) NOT NULL,
    comentarios VARCHAR(255) NULL,
    CONSTRAINT pk_reservacion PRIMARY KEY (id_reservacion),
    CONSTRAINT fk_reservacion_usuarios
        FOREIGN KEY (no_empleado) REFERENCES Usuarios(no_empleado)
);

CREATE TABLE Lista_Espera (
    id_lista INT NOT NULL AUTO_INCREMENT,
    no_empleado INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    no_personas INT NOT NULL,
    tipo_festejo VARCHAR(50) NULL,
    hora_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'EN_ESPERA',
    CONSTRAINT pk_lista PRIMARY KEY (id_lista),
    CONSTRAINT fk_lista_espera_usuarios
        FOREIGN KEY (no_empleado) REFERENCES Usuarios(no_empleado)
);

CREATE TABLE Promocion (
    id_promocion INT NOT NULL AUTO_INCREMENT,
    no_empleado INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    vigencia_inicio DATE NOT NULL,
    vigencia_fin DATE NOT NULL,
    estado TINYINT(1) NOT NULL DEFAULT 1,
    ocasion VARCHAR(30) NULL,
    dias_vigentes VARCHAR(100) NOT NULL,
    condiciones VARCHAR(255) NULL,
    CONSTRAINT pk_promocion PRIMARY KEY (id_promocion),
    CONSTRAINT fk_promocion_usuarios
        FOREIGN KEY (no_empleado) REFERENCES Usuarios(no_empleado)
);

CREATE TABLE Gestion_de_meseros (
    id_gestion INT NOT NULL AUTO_INCREMENT,
    no_empleado INT NOT NULL,
    id_mesa INT NULL,
    promedio DOUBLE DEFAULT 0,
    ranking INT DEFAULT 0,
    turno VARCHAR(30) NULL,
    observacion VARCHAR(255) NULL,
    calificacion DOUBLE DEFAULT 0,
    fecha_registro DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT pk_meseros PRIMARY KEY (id_gestion),
    CONSTRAINT fk_gestion_usuarios
        FOREIGN KEY (no_empleado) REFERENCES Usuarios(no_empleado),
    CONSTRAINT fk_gestion_mesa
        FOREIGN KEY (id_mesa) REFERENCES Mesa(id_mesa)
);

CREATE TABLE Promocion_has_Gestion_de_meseros (
    id_promocion INT NOT NULL,
    id_gestion INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    fecha_aplicacion DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT pk_promo_meseros PRIMARY KEY (id_promocion, id_gestion),
    CONSTRAINT fk_pg_promocion
        FOREIGN KEY (id_promocion) REFERENCES Promocion(id_promocion),
    CONSTRAINT fk_pg_gestion
        FOREIGN KEY (id_gestion) REFERENCES Gestion_de_meseros(id_gestion)
);

-- ============================================================
-- DATOS SEMILLA (desarrollo/pruebas)
--
-- Roles y usuarios de nombre_usuario/contrasena en texto plano:
-- backend/auth.py compara contrasena como texto plano, no hash.
-- No se incluye rol de Administrador (se retiró del sistema).
-- ============================================================

-- 1. Insertar Roles
INSERT INTO Rol (id_rol, nombre) VALUES
('GER', 'GERENTE'),
('MES', 'MESERO'),
('REC', 'HOSTESS'),
('JDP', 'JEFEDEPISO');

-- 2. Insertar Usuarios
INSERT INTO Usuarios (no_empleado, id_rol, nombre, apellido, contrasena, correo, nombre_usuario, estado, ultimo_acceso) VALUES
(102, 'GER', 'Roberto', 'González', 'gerente123', 'roberto.g@norestegrill.com', 'gerente', 'ACTIVO', NOW()),
(103, 'MES', 'Carlos', 'Mendoza', 'mesero123', 'carlos.m@norestegrill.com', 'mesero', 'ACTIVO', NOW()),
(104, 'JDP', 'Sofia', 'Ramírez', 'jefepiso123', 'sofia.r@norestegrill.com', 'jefepiso', 'ACTIVO', NOW()),
(105, 'REC', 'Valeria', 'Torres', 'hostess123', 'valeria.t@norestegrill.com', 'hostess', 'ACTIVO', NOW());

-- 3. Insertar Mesas
INSERT INTO Mesa (id_mesa, no_empleado, estado, nombre_cliente, no_personas, hora_inicio, razon_retraso, comentario_retraso) VALUES
(1, 103, 'ocupada', 'Familia Gómez', 4, NOW(), NULL, NULL),
(2, 104, 'ocupada', 'Juan Pérez', 2, NOW(), NULL, NULL),
(3, NULL, 'libre', NULL, NULL, NULL, NULL, NULL),
(4, NULL, 'reservada', 'Alejandro Silva', 6, NULL, NULL, NULL),
(5, 103, 'retraso', 'Lucía Méndez', 3, NOW(), 'Cocina saturada', 'Espera prolongada en corte de carne');

-- 4. Insertar Reservaciones
INSERT INTO Reservacion (no_empleado, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios) VALUES
(105, 'Alejandro', 'Silva', '8441234567', CURRENT_DATE, '20:00:00', 6, 'CONFIRMADA', 'Mesa cerca de la terraza'),
(105, 'Mariana', 'López', '8449876543', CURRENT_DATE, '21:30:00', 2, 'PENDIENTE', 'Cumpleaños'),
(105, 'Fernando', 'Castillo', '8445551234', CURRENT_DATE + INTERVAL 1 DAY, '14:00:00', 4, 'CONFIRMADA', NULL);

-- 5. Insertar Lista de Espera
INSERT INTO Lista_Espera (no_empleado, nombre, no_personas, tipo_festejo, estado) VALUES
(105, 'Ricardo Treviño', 4, 'Aniversario', 'EN_ESPERA'),
(105, 'Beatriz Garza', 2, NULL, 'EN_ESPERA'),
(105, 'Guillermo Ruiz', 8, 'Cumpleaños', 'SENTADO');

-- 6. Insertar Promociones
INSERT INTO Promocion (no_empleado, nombre, descripcion, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes, condiciones) VALUES
(102, '2x1 en Ribeye', '2x1 en cortes de Ribeye de 400g', CURRENT_DATE, CURRENT_DATE + INTERVAL 30 DAY, 1, 'Jueves de Cortes', 'Jueves', 'Válido solo en consumo en restaurante'),
(102, 'Margarita Happy Hour', 'Margaritas al 2x1 de 5 PM a 8 PM', CURRENT_DATE, CURRENT_DATE + INTERVAL 60 DAY, 1, 'Happy Hour', 'Lunes,Martes,Miércoles', 'No acumulable con otras promociones'),
(102, 'Postre Gratis Cumpleañero', 'Postre de la casa gratis mostrando INE', CURRENT_DATE, CURRENT_DATE + INTERVAL 365 DAY, 1, 'Cumpleaños', 'Lunes,Martes,Miércoles,Jueves,Viernes,Sábado,Domingo', 'Consumo mínimo de $500');

-- 7. Insertar Gestión de Meseros
INSERT INTO Gestion_de_meseros (no_empleado, id_mesa, promedio, ranking, turno, observacion, calificacion) VALUES
(103, 1, 4.8, 1, 'Matutino', 'Excelente atención y rapidez', 5.0),
(104, 2, 4.2, 2, 'Matutino', 'Buen servicio general', 4.5);

-- 8. Insertar Promocion_has_Gestion_de_meseros
INSERT INTO Promocion_has_Gestion_de_meseros (id_promocion, id_gestion, cantidad) VALUES
(1, 1, 2),
(2, 2, 4);

-- Query de verificación rápida
SELECT u.nombre_usuario, r.nombre AS rol, m.id_mesa, m.estado AS estado_mesa
FROM Usuarios u
JOIN Rol r ON u.id_rol = r.id_rol
LEFT JOIN Mesa m ON u.no_empleado = m.no_empleado;
