# Noreste Grill

Aplicacion Flask para la operacion interna de un restaurante: inicio de sesion por rol, dashboards, usuarios, reservaciones, lista de espera, estado de mesas, promociones, rendimiento de meseros y reportes de mesas/retrasos agregados en Sprint 1.

## Stack Tecnologico

| Area | Tecnologia |
| --- | --- |
| Backend | Python + Flask |
| Frontend | HTML, CSS, JavaScript |
| Base de datos | MySQL 8 |
| Contenedores de desarrollo | Docker + Docker Compose |
| Documentacion API | Swagger UI en `/docs` |
| Conexion a base de datos | mysql-connector-python |
| Reportes PDF | ReportLab |

## Funcionalidad de Sprint 1

- Stack Docker de desarrollo con servicios separados para Flask y MySQL.
- Inicializacion automatica de MySQL desde `database/schema.sql` la primera vez que se crea el volumen.
- Endpoints de reportes de mesas/retrasos para resumenes operativos.
- Generacion de reportes PDF de mesas/retrasos con ReportLab.
- Swagger UI disponible en `http://127.0.0.1:5000/docs`.

## Setup Recomendado: Docker

Requisito: instalar Docker Desktop con Docker Compose.

1. Copiar el archivo de variables de entorno:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Revisar `.env`. Los valores del ejemplo son placeholders seguros para desarrollo local.

3. Levantar Flask y MySQL:

   ```powershell
   docker compose up --build
   ```

4. Abrir la aplicacion:

   ```text
   http://127.0.0.1:5000
   ```

5. Abrir Swagger UI:

   ```text
   http://127.0.0.1:5000/docs
   ```

Con Docker, los integrantes del equipo no necesitan instalar MySQL por separado. El contenedor de MySQL crea la base configurada y ejecuta `database/schema.sql` automaticamente la primera vez que se crea el volumen `mysql_data`.

## Detener Docker

Detener los contenedores conservando el volumen local de base de datos:

```powershell
docker compose down
```

Detener los contenedores y borrar el volumen local de base de datos:

```powershell
docker compose down -v
```

Advertencia: `docker compose down -v` elimina el volumen local de MySQL. El siguiente `docker compose up --build` recreara la base desde `database/schema.sql`, perdiendo los cambios locales.

## Variables de Entorno

`docker-compose.yml` lee valores locales desde `.env`.

| Variable | Usada por | Proposito |
| --- | --- | --- |
| `DB_HOST` | Flask | Host de MySQL. En Docker debe ser `db`. |
| `DB_NAME` | Flask + MySQL | Nombre de la base de datos de la aplicacion. |
| `DB_USER` | Flask + MySQL | Usuario de base de datos de la aplicacion. |
| `DB_PASSWORD` | Flask + MySQL | Password del usuario de la aplicacion. |
| `MYSQL_ROOT_PASSWORD` | MySQL | Password root/admin del contenedor MySQL. |

No commitear un `.env` real; Git y Docker lo ignoran.

## Setup Manual Opcional

El setup manual solo es util si no se usa Docker.

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Para setup manual, instalar e iniciar MySQL localmente, crear una base de datos, ejecutar `database/schema.sql` dentro de esa base y configurar `DB_HOST=localhost` en el `.env` local.

Ejecutar Flask manualmente:

```powershell
python -m backend.test_app
```

## Roles

| Rol | Proposito |
| --- | --- |
| Gerente | Administra usuarios y promociones, revisa reservaciones y consulta indicadores generales. |
| Jefe de piso | Supervisa estado de mesas, operacion del piso, personal y reservaciones. |
| Hostess | Gestiona reservaciones, lista de espera, asignacion de mesas y promociones activas. |
| Mesero | Consulta mesas asignadas, promociones activas y rendimiento personal. |

Ver [ONBOARDING.md](ONBOARDING.md) para estructura del proyecto, notas de setup, rutas y detalles operativos.
