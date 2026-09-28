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
  errors.py
  openapi_spec.py
  controllers/      -> rutas Flask (Blueprints): reciben el request y devuelven la respuesta
  services/         -> logica de negocio, validaciones y permisos por rol
  repositories/      -> Data Access Layer: unicas funciones que ejecutan SQL

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

| Carpeta o archivo | Que contiene | Para que sirve |
| --- | --- | --- |
| `backend/` | Archivos `.py` del servidor | Contiene la logica principal de Flask, las rutas, APIs y conexion a la base de datos |
| `backend/test_app.py` | Aplicacion principal de Flask | Crea `app`, registra los blueprints (controllers) y define la ruta inicial `/` |
| `backend/db.py` | Configuracion de conexion a MySQL | Centraliza la conexion para que los repositories puedan consultar la base de datos |
| `backend/errors.py` | `ServiceError` | Excepcion de negocio que un errorhandler central convierte en `{"ok": false, "message": ...}` |
| `backend/openapi_spec.py` | Generador de OpenAPI | Construye el spec que consume Swagger UI en `/docs` a partir de las rutas registradas |
| `backend/controllers/*.py` | Capa Controller | Un Blueprint por modulo (auth, usuarios, reservaciones, etc). Recibe el request, llama al service y arma el `jsonify()` |
| `backend/services/*.py` | Capa Service | Reglas de negocio: validaciones, permisos por rol, formateo de fechas/horas. No ejecuta SQL directamente |
| `backend/repositories/*.py` | Data Access Layer | Unico lugar donde se ejecutan queries SQL contra MySQL |
| `templates/` | Archivos `.html` | Contiene las pantallas que Flask renderiza con `render_template()` |
| `static/CSS/` | Archivos de estilos | Define el diseno visual de login, dashboards y modulos |
| `static/JS/` | Archivos JavaScript | Hace peticiones `fetch()` a las APIs y controla la interaccion de las vistas |
| `static/IMAGES/` | Imagenes del sistema | Guarda recursos visuales como el logo |
| `database/` | Scripts SQL | Contiene `schema.sql` para crear la base de datos y tablas |
| `requirements.txt` | Lista de dependencias | Permite instalar las librerias necesarias con `pip install -r requirements.txt` |
| `.env.example` | Ejemplo de variables de entorno | Muestra que datos se necesitan para conectar a MySQL sin subir credenciales reales |
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

El archivo `.env.example` contiene valores seguros de desarrollo. Cada persona puede ajustar su `.env` local, pero no debe commitearlo. Revisar siguiente sección de la estructura esperada en la base de datos.

Variables usadas:

| Variable | Uso |
| --- | --- |
| `DB_HOST` | Host de MySQL para Flask. En Docker debe ser `db`. |
| `DB_NAME` | Nombre de la base de datos de la aplicacion. |
| `DB_USER` | Usuario de MySQL que usa Flask. |
| `DB_PASSWORD` | Password del usuario de aplicacion. |
| `MYSQL_ROOT_PASSWORD` | Password root/admin del contenedor MySQL. |

Ejemplo para PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="tu_contrasena"
$env:DB_NAME="noreste_grill"
```

Nota: no se deben subir credenciales reales a GitHub. El archivo `.env.example` solo sirve como referencia.

#### Estructura esperada de la base de datos

El proyecto incluye el script `database/schema.sql` con la creacion de la base de datos `noreste_grill` y sus tablas principales. Para correrlo localmente, primero se debe ejecutar ese script en MySQL.

Ejemplo desde MySQL Workbench:

1. Abrir MySQL Workbench.
2. Conectarse al servidor local.
3. Abrir el archivo `database/schema.sql`.
4. Ejecutar el script completo.

Ejemplo desde terminal si el comando `mysql` esta disponible:

```powershell
mysql -u root -p < database/schema.sql
```

Nota: el script crea la estructura de tablas, pero no agrega automaticamente usuarios, roles, mesas o promociones iniciales.

Tablas principales:

| Tabla | Para que se usa |
| --- | --- |
| `Rol` | Guarda los roles disponibles del sistema |
| `Usuarios` | Guarda usuarios, datos personales, contrasena, estado y rol |
| `Reservacion` | Guarda reservaciones por cliente, fecha, hora y personas |
| `Lista_Espera` | Guarda clientes en espera y su estado |
| `Mesa` | Guarda estado de mesas, cliente asignado, mesero y tiempos |
| `Promocion` | Guarda promociones, vigencia, condiciones y estado |
| `Gestion_de_meseros` | Guarda rendimiento, mesas atendidas, turno, observaciones y calificacion |
| `Promocion_has_Gestion_de_meseros` | Relaciona promociones aplicadas con la gestion del mesero |

Campos importantes por tabla:

| Tabla | Campos usados por el codigo |
| --- | --- |
| `Rol` | `id_rol`, `nombre` |
| `Usuarios` | `no_empleado`, `id_rol`, `nombre`, `apellido`, `contrasena`, `correo`, `nombre_usuario`, `estado`, `ultimo_acceso` |
| `Reservacion` | `id_reservacion`, `nombre_cliente`, `no_personas`, `fecha`, `hora`, `telefono`, `estado`, `comentarios` |
| `Lista_Espera` | `id_lista`, `nombre_cliente`, `no_personas`, `telefono`, `estado`, `hora_registro` |
| `Mesa` | `id_mesa`, `no_empleado`, `estado`, `nombre_cliente`, `no_personas`, `hora_inicio`, `razon_retraso`, `comentario_retraso` |
| `Promocion` | `id_promocion`, `no_empleado`, `nombre`, `descripcion`, `condiciones`, `vigencia_inicio`, `vigencia_fin`, `estado`, `ocasion`, `dias_vigentes` |
| `Gestion_de_meseros` | `id_gestion`, `no_empleado`, `id_mesa`, `promedio`, `ranking`, `turno`, `observacion`, `calificacion`, `fecha_registro` |
| `Promocion_has_Gestion_de_meseros` | `id_promocion`, `id_gestion`, `cantidad`, `fecha_aplicacion` |

#### Credenciales

##### Credenciales de MySQL

Las credenciales de MySQL dependen de la computadora donde se instale el proyecto. Normalmente se usa:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=contrasena_local
DB_NAME=noreste_grill
```

La contrasena real no debe quedar escrita en la documentacion ni en commits publicos.

#### Credenciales de usuarios del sistema

El login de la aplicacion usa la tabla `Usuarios`. Para entrar al sistema debe existir al menos un usuario activo en esa tabla.

El backend valida:

```text
nombre_usuario
contrasena
estado = ACTIVO
rol asociado en la tabla Rol
```

Las contrasenas se comparan directamente contra el campo `contrasena` de la tabla `Usuarios`.

#### Roles del sistema

Los roles principales son:

| Rol | Codigo usado | Funcion general |
| --- | --- | --- |
| Gerente | `GERENTE` / `G` | Administracion general del sistema |
| Jefe de piso | `JEFEDEPISO` o `JEFEPISO` / `JP` | Supervision operativa |
| Hostess | `HOSTESS` / `H` | Recepcion, lista de espera, reservaciones y mesas |
| Mesero | `MESERO` / `M` | Consulta de mesas asignadas y promociones vigentes |

Al iniciar sesion, el frontend guarda datos en `localStorage`:

```text
ROL
USER
NO_EMPLEADO
```

Con el valor de `ROL`, la aplicacion redirige al dashboard correspondiente.

#### Funcionamiento de roles

##### Gerente

El gerente tiene acceso a funciones administrativas como:

```text
/gerente
/usuarios
/reservaciones
/gestion_promociones
/personal
```

Puede administrar usuarios y promociones, revisar reservaciones y consultar indicadores generales.

##### Jefe de piso

El jefe de piso tiene acceso a supervision operativa:

```text
/jefepiso
/estado_mesas
/personal
/reservaciones
/usuarios
```

En usuarios, el jefe de piso tiene restricciones. Puede trabajar principalmente con personal operativo, pero no debe modificar cuentas de gerente.

##### Hostess

La hostess trabaja con recepcion:

```text
/hostess
/reservaciones
/lista_espera
/estado_mesas
/promociones_vigentes
```

Su flujo principal es revisar reservaciones, manejar la lista de espera, asignar clientes a mesas y consultar promociones vigentes.

##### Mesero

El mesero tiene acceso a:

```text
/mesero
/estado_mesas
/promociones_vigentes
/rendimiento_mesero
```

Puede revisar sus mesas asignadas, ver promociones vigentes y consultar su rendimiento.

#### Modulos principales del backend

Cada modulo (auth, usuarios, reservaciones, lista_espera, mesas, promociones, meseros y los 4 dashboards) esta dividido en tres archivos, uno por capa:

| Capa | Archivo tipico | Responsabilidad |
| --- | --- | --- |
| Controller | `backend/controllers/<modulo>_controller.py` | Define las rutas del Blueprint, lee `request`, llama al service y devuelve `jsonify()` |
| Service | `backend/services/<modulo>_service.py` | Valida datos, aplica reglas de negocio (permisos por rol, formatos) y orquesta el repository |
| Repository | `backend/repositories/<modulo>_repository.py` | Ejecuta las queries SQL contra MySQL y regresa filas/valores simples |

`backend/test_app.py` crea la app Flask, registra los controllers como blueprints y registra el errorhandler de `ServiceError`. `backend/db.py` centraliza la conexion a MySQL.

##### Promociones

Las promociones se guardan en la tabla `Promocion`.

Cada promocion puede tener:

```text
nombre
descripcion
condiciones
vigencia_inicio
vigencia_fin
estado
ocasion
dias_vigentes
```

El sistema distingue entre:

| Vista/API | Funcion |
| --- | --- |
| `/gestion_promociones` | Administrar promociones |
| `/promociones_vigentes` | Consultar promociones activas |
| `/api/promociones` | Crear, consultar y editar promociones |
| `/api/promociones-vigentes` | Consultar promociones activas dentro de su vigencia |

Si una promocion ya fue aplicada por un mesero, el sistema puede desactivarla en lugar de eliminarla para no romper registros historicos.

##### Gestion de meseros

La gestion de meseros usa principalmente:

```text
Gestion_de_meseros
Promocion_has_Gestion_de_meseros
Mesa
Usuarios
```

El sistema calcula o consulta:

```text
mesas atendidas
mesas asignadas
promedio de tiempo
promociones aplicadas
calificacion
ranking
turno
observaciones
```

Cuando una mesa ocupada pasa a `libre`, el backend registra una entrada en `Gestion_de_meseros` para contar esa mesa como atendida y calcular el tiempo de servicio.

##### Estado de mesas

El modulo de mesas maneja estados como:

```text
libre
ocupada
limpieza
```

Tambien guarda:

```text
cliente asignado
numero de personas
mesero asignado
hora de inicio
razon de retraso
comentario de retraso
```

El endpoint principal es:

```text
/api/mesas
```

##### Reservaciones y lista de espera

Reservaciones:

```text
/reservaciones
/api/reservaciones
```

Lista de espera:

```text
/lista_espera
/api/lista-espera
```

Estos modulos permiten registrar, editar, eliminar y consultar clientes antes de asignarlos a una mesa.


### 3. Como correr el proyecto

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
