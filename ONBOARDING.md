# Onboarding del proyecto

Este documento explica lo necesario para entender, instalar y correr localmente el sistema de gestion de Noreste Grill.

## Descripcion general

El proyecto es una aplicacion web hecha con Flask para apoyar la operacion de un restaurante. Incluye inicio de sesion, dashboards por rol, administracion de usuarios, reservaciones, lista de espera, estado de mesas, promociones y gestion de meseros.

La aplicacion usa:

| Parte | Tecnologia |
| --- | --- |
| Backend | Python + Flask |
| Frontend | HTML, CSS y JavaScript |
| Base de datos | MySQL |
| Conexion a BD | mysql-connector-python |
| Organizacion backend | Blueprints de Flask dentro de `backend/` |

## Estructura del proyecto

```text
backend/
  __init__.py
  test_app.py
  db.py
  auth.py
  usuarios.py
  reservaciones.py
  lista_espera.py
  mesas.py
  promociones.py
  meseros.py
  dashboard_gerente.py
  dashboard_hostess.py
  dashboard_jefepiso.py
  dashboard_mesero.py

templates/
  Archivos HTML de las vistas

static/
  CSS/
  JS/
  IMAGES/

README.md
VERSIONES.md
requirements.txt
.env.example
```

El archivo principal de Flask es:

```text
backend/test_app.py
```

Este archivo registra todos los blueprints y conecta Flask con las carpetas `templates/` y `static/`.

## Instalacion local

### 1. Instalar Python

Instalar Python desde:

```text
https://www.python.org/downloads/
```

Durante la instalacion en Windows, activar la opcion **Add Python to PATH**.

Verificar la instalacion:

```powershell
python --version
```

### 2. Crear entorno virtual

Desde la carpeta raiz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar librerias

```powershell
pip install -r requirements.txt
```

Las librerias principales son:

```text
Flask
mysql-connector-python
waitress
```

Las versiones exactas estan documentadas en `VERSIONES.md`.

### 4. Instalar MySQL

Instalar MySQL desde:

```text
https://dev.mysql.com/downloads/installer/
```

Tambien se recomienda instalar MySQL Workbench para administrar la base de datos de forma visual.

## Base de datos

El proyecto espera una base de datos llamada:

```text
noreste_grill
```

La conexion se configura en:

```text
backend/db.py
```

Las variables usadas son:

| Variable | Descripcion |
| --- | --- |
| `DB_HOST` | Servidor donde corre MySQL, normalmente `localhost` |
| `DB_USER` | Usuario de MySQL |
| `DB_PASSWORD` | Contrasena del usuario de MySQL |
| `DB_NAME` | Nombre de la base de datos, normalmente `noreste_grill` |

Ejemplo para PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="tu_contrasena"
$env:DB_NAME="noreste_grill"
```

Nota: no se deben subir credenciales reales a GitHub. El archivo `.env.example` solo sirve como referencia.

## Estructura esperada de la base de datos

El proyecto no incluye todavia un archivo `.sql` con la creacion completa de tablas. Para correrlo localmente, la base de datos debe existir y tener las tablas que usa el backend.

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

## Credenciales

### Credenciales de MySQL

Las credenciales de MySQL dependen de la computadora donde se instale el proyecto. Normalmente se usa:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=contrasena_local
DB_NAME=noreste_grill
```

La contrasena real no debe quedar escrita en la documentacion ni en commits publicos.

### Credenciales de usuarios del sistema

El login de la aplicacion usa la tabla `Usuarios`. Para entrar al sistema debe existir al menos un usuario activo en esa tabla.

El backend valida:

```text
nombre_usuario
contrasena
estado = ACTIVO
rol asociado en la tabla Rol
```

Las contrasenas se comparan directamente contra el campo `contrasena` de la tabla `Usuarios`.

## Roles del sistema

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

## Funcionamiento de roles

### Gerente

El gerente tiene acceso a funciones administrativas como:

```text
/gerente
/usuarios
/reservaciones
/gestion_promociones
/personal
```

Puede administrar usuarios y promociones, revisar reservaciones y consultar indicadores generales.

### Jefe de piso

El jefe de piso tiene acceso a supervision operativa:

```text
/jefepiso
/estado_mesas
/personal
/reservaciones
/usuarios
```

En usuarios, el jefe de piso tiene restricciones. Puede trabajar principalmente con personal operativo, pero no debe modificar cuentas de gerente.

### Hostess

La hostess trabaja con recepcion:

```text
/hostess
/reservaciones
/lista_espera
/estado_mesas
/promociones_vigentes
```

Su flujo principal es revisar reservaciones, manejar la lista de espera, asignar clientes a mesas y consultar promociones vigentes.

### Mesero

El mesero tiene acceso a:

```text
/mesero
/estado_mesas
/promociones_vigentes
/rendimiento_mesero
```

Puede revisar sus mesas asignadas, ver promociones vigentes y consultar su rendimiento.

## Modulos principales del backend

| Archivo | Funcion |
| --- | --- |
| `backend/test_app.py` | Crea la app Flask y registra los blueprints |
| `backend/db.py` | Centraliza la conexion a MySQL |
| `backend/auth.py` | Login y validacion de usuario |
| `backend/usuarios.py` | CRUD de usuarios y restricciones por rol |
| `backend/reservaciones.py` | CRUD de reservaciones |
| `backend/lista_espera.py` | Manejo de clientes en espera |
| `backend/mesas.py` | Estado de mesas, asignacion de meseros y registro de tiempos |
| `backend/promociones.py` | CRUD de promociones y promociones vigentes |
| `backend/meseros.py` | Rendimiento, ranking, turnos, observaciones y promociones aplicadas |
| `backend/dashboard_*.py` | Datos resumidos para cada dashboard |

## Promociones

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

## Gestion de meseros

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

## Estado de mesas

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

## Reservaciones y lista de espera

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

## Como correr el proyecto

Desde la raiz del proyecto:

```powershell
.\venv\Scripts\activate
```

Configurar variables de entorno:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="tu_contrasena"
$env:DB_NAME="noreste_grill"
```

Ejecutar Flask:

```powershell
python -m backend.test_app
```

Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Rutas principales

| Ruta | Vista |
| --- | --- |
| `/` | Login |
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

## Flujo general de uso

1. El usuario entra al login.
2. El frontend manda `nombre_usuario` y `contrasena` a `/api/login`.
3. El backend busca el usuario en `Usuarios` y su rol en `Rol`.
4. Si el usuario existe, la contrasena coincide y esta activo, el frontend guarda los datos en `localStorage`.
5. Segun el rol, se redirige al dashboard correspondiente.
6. Desde el dashboard se accede a los modulos permitidos para ese rol.

## Cosas importantes para alguien nuevo

- La app debe correrse desde la raiz con `python -m backend.test_app`.
- La base de datos MySQL debe estar creada antes de iniciar Flask.
- Las rutas del frontend usan URLs como `/api/usuarios`, `/api/mesas` y `/api/promociones`.
- Los archivos HTML estan en `templates/`.
- Los estilos, scripts e imagenes estan en `static/`.
- El rol del usuario se guarda en `localStorage`, por eso algunas pantallas dependen de haber iniciado sesion.
- No hay migraciones automaticas ni archivo `.sql` incluido todavia.
- No se debe subir el entorno virtual `venv/` ni archivos `.env` reales.

## Recomendaciones para continuar el proyecto

- Agregar un archivo `schema.sql` con la estructura completa de la base de datos.
- Agregar datos iniciales para roles y un usuario administrador de prueba.
- Cambiar el manejo de contrasenas para usar hashing en lugar de texto plano.
- Agregar validaciones de sesion desde backend, no solo desde `localStorage`.
- Separar configuracion de desarrollo y produccion si se va a desplegar.
