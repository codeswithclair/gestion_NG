# Onboarding del proyecto

Este documento explica como entender, instalar y correr localmente el sistema de gestion de Noreste Grill.

## Descripcion general

La aplicacion es un sistema web interno para la operacion de un restaurante. Incluye inicio de sesion, dashboards por rol, administracion de usuarios, reservaciones, lista de espera, estado de mesas, promociones, gestion de meseros y reportes de mesas/retrasos en PDF.

## Stack principal

| Parte | Tecnologia |
| --- | --- |
| Backend | Python + Flask |
| Frontend | HTML, CSS y JavaScript |
| Base de datos | MySQL 8 |
| Entorno recomendado | Docker Desktop + Docker Compose |
| Conexion a BD | mysql-connector-python |
| Documentacion API | Swagger UI en `/docs` |
| Reportes PDF | ReportLab |

## Estructura del proyecto

```text
backend/
  test_app.py
  db.py
  controllers/
  services/
  repositories/

templates/
static/
database/
  schema.sql

Dockerfile
docker-compose.yml
.dockerignore
.env.example
requirements.txt
README.md
VERSIONES.md
```

| Ruta | Proposito |
| --- | --- |
| `backend/test_app.py` | Crea la app Flask, registra blueprints y expone Swagger UI. |
| `backend/db.py` | Lee variables de entorno y centraliza la conexion a MySQL. |
| `backend/controllers/` | Rutas Flask/API. |
| `backend/services/` | Reglas de negocio y formateo. |
| `backend/repositories/` | Consultas SQL contra MySQL. |
| `templates/` | HTML renderizado por Flask. |
| `static/` | CSS, JavaScript e imagenes. |
| `database/schema.sql` | Tablas y datos semilla para desarrollo. |

## Setup recomendado con Docker

Con Docker, cada integrante solo necesita Docker Desktop. No es necesario instalar MySQL localmente ni crear la base de datos a mano.

### 1. Instalar Docker Desktop

Instalar Docker Desktop y confirmar que Docker Compose este disponible:

```powershell
docker --version
docker compose version
```

### 2. Crear `.env`

Copiar el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

El archivo `.env.example` contiene valores seguros de desarrollo. Cada persona puede ajustar su `.env` local, pero no debe commitearlo.

Variables usadas:

| Variable | Uso |
| --- | --- |
| `DB_HOST` | Host de MySQL para Flask. En Docker debe ser `db`. |
| `DB_NAME` | Nombre de la base de datos de la aplicacion. |
| `DB_USER` | Usuario de MySQL que usa Flask. |
| `DB_PASSWORD` | Password del usuario de aplicacion. |
| `MYSQL_ROOT_PASSWORD` | Password root/admin del contenedor MySQL. |

### 3. Levantar la aplicacion

Desde la raiz del proyecto:

```powershell
docker compose up --build
```

Abrir:

```text
http://127.0.0.1:5000
```

Swagger UI:

```text
http://127.0.0.1:5000/docs
```

### 4. Detener contenedores

Detener Flask y MySQL sin borrar la base local:

```powershell
docker compose down
```

Detener contenedores y borrar tambien el volumen local de MySQL:

```powershell
docker compose down -v
```

Advertencia: `docker compose down -v` borra el volumen `mysql_data`. Eso elimina los datos locales de MySQL. La siguiente vez que se ejecute `docker compose up --build`, MySQL volvera a inicializar la base desde `database/schema.sql`.

## Inicializacion de MySQL en Docker

`docker-compose.yml` monta:

```text
./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro
```

El contenedor oficial de MySQL ejecuta los scripts de `/docker-entrypoint-initdb.d/` solo la primera vez que crea su directorio de datos. El nombre de la base se toma de `MYSQL_DATABASE`, que Compose recibe desde `DB_NAME` en `.env`.

No agregues `CREATE DATABASE` ni `USE` al inicio de `schema.sql` para el flujo Docker; MySQL ya ejecuta ese script dentro de la base creada por `MYSQL_DATABASE`.

## Setup manual opcional sin Docker

Usar este camino solo si no se quiere usar Docker.

1. Instalar Python.
2. Instalar MySQL Server localmente.
3. Crear y activar entorno virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. Instalar dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

5. Crear `.env` con `DB_HOST=localhost` y credenciales de tu MySQL local.
6. Crear la base de datos manualmente en MySQL.
7. Ejecutar `database/schema.sql` dentro de esa base.
8. Correr Flask:

   ```powershell
   python -m backend.test_app
   ```

## Credenciales de desarrollo

`database/schema.sql` incluye datos semilla para desarrollo/pruebas, incluyendo usuarios de aplicacion con passwords en texto plano. Esto se conserva por ahora para Sprint 1 y no debe tratarse como configuracion de produccion.

## Rutas principales

| Ruta | Vista |
| --- | --- |
| `/` | Login |
| `/docs` | Swagger UI |
| `/gerente` | Dashboard de gerente |
| `/hostess` | Dashboard de hostess |
| `/jefepiso` | Dashboard de jefe de piso |
| `/mesero` | Dashboard de mesero |
| `/usuarios` | Gestion de usuarios |
| `/reservaciones` | Gestion de reservaciones |
| `/lista_espera` | Lista de espera |
| `/estado_mesas` | Estado de mesas |
| `/gestion_promociones` | Gestion de promociones |
| `/promociones_vigentes` | Promociones vigentes |
| `/personal` | Gestion de meseros |
| `/rendimiento_mesero` | Rendimiento individual del mesero |

## Modulos principales

| Modulo | Funcion |
| --- | --- |
| Auth | Login, validacion de usuario, estado y rol. |
| Usuarios | Alta, consulta, edicion y baja logica/fisica segun reglas. |
| Reservaciones | Gestion de reservaciones. |
| Lista de espera | Clientes pendientes antes de asignar mesa. |
| Mesas | Estado, cliente, mesero, timers, retrasos y reportes. |
| Promociones | Promociones activas y administracion. |
| Meseros | Rendimiento, turnos, ranking y promociones aplicadas. |
| Dashboards | Resumenes para gerente, hostess, jefe de piso y mesero. |

## Cosas importantes para alguien nuevo

- El setup recomendado es Docker Desktop + Docker Compose.
- Con Docker no hace falta instalar MySQL localmente.
- `.env.example` se commitea; `.env` no.
- `docker compose down` conserva la base local.
- `docker compose down -v` borra la base local.
- `database/schema.sql` si existe y contiene la estructura y datos semilla.
- La app usa el servidor de desarrollo de Flask en Sprint 1.
- Waitress/produccion quedan para Sprint 2.
- El rol del usuario se guarda en `localStorage`, por eso algunas pantallas dependen de haber iniciado sesion.

## Recomendaciones futuras

- Separar configuracion de desarrollo y produccion.
- Cambiar passwords de usuarios de aplicacion a hashing.
- Agregar migraciones de base de datos.
- Reemplazar el servidor de desarrollo Flask por Waitress u otro servidor WSGI en Sprint 2.
