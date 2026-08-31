# Noreste Grill

Aplicación Flask para los flujos de trabajo del personal de un restaurante, incluyendo inicio de sesión, reservaciones, lista de espera, mesas, promociones, usuarios y dashboards.

## Usuarios objetivo

La aplicación está pensada para el personal interno del restaurante, no para clientes finales. Los roles que la usan son:

| Rol | Quién es | Para qué usa la aplicación |
| --- | --- | --- |
| Gerente | Encargado general del restaurante | Administra usuarios, promociones, revisa reservaciones y consulta indicadores generales del negocio |
| Jefe de piso | Supervisor operativo del salón | Supervisa el estado de las mesas, el personal operativo y las reservaciones del turno |
| Hostess | Personal de recepción | Recibe clientes, gestiona la lista de espera, las reservaciones y la asignación de mesas |
| Mesero | Personal de servicio en mesas | Consulta sus mesas asignadas, las promociones vigentes y su propio rendimiento |

Cada rol inicia sesión con su propio usuario y es redirigido automáticamente a su dashboard correspondiente. Más detalle sobre permisos y rutas por rol en [ONBOARDING.md](ONBOARDING.md).

## Instalación local

Crear y activar un entorno virtual, luego instalar las dependencias:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Configurar el archivo .env

La aplicación usa [python-dotenv](https://pypi.org/project/python-dotenv/) para leer la configuración de la base de datos desde un archivo `.env`. Este archivo **no se sube al repositorio** (está en `.gitignore`) porque contiene credenciales locales.

### Pasos para configurarlo

1. En la raíz del proyecto existe un archivo de ejemplo llamado `.env.example`. Cópialo y renómbralo a `.env`:

   ```powershell
   Copy-Item .env.example .env
   ```

2. Abre el archivo `.env` recién creado y reemplaza los valores con los datos de tu instalación local de MySQL:

   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=tu_contrasena_de_mysql
   DB_NAME=noreste_grill
   ```

3. Guarda el archivo. `backend/db.py` carga estas variables automáticamente al iniciar la aplicación (con `load_dotenv()`), así que no es necesario declararlas manualmente en la terminal cada vez.

### Variables disponibles

| Variable | Descripción | Valor por defecto si falta |
| --- | --- | --- |
| `DB_HOST` | Servidor donde corre MySQL | `localhost` |
| `DB_USER` | Usuario de MySQL | `root` |
| `DB_PASSWORD` | Contraseña del usuario de MySQL | (vacío) |
| `DB_NAME` | Nombre de la base de datos | `noreste_grill` |

### Notas importantes

- El archivo `.env` es **personal de cada máquina**: nunca debe compartirse ni subirse a control de versiones.
- Si el archivo `.env` no existe o le falta alguna variable, la aplicación usará los valores por defecto de la tabla anterior (definidos en `backend/db.py`), lo cual puede causar errores de conexión si tu instalación de MySQL no coincide con esos valores.
- Antes de correr la app por primera vez, la base de datos `noreste_grill` debe existir en MySQL (ver [ONBOARDING.md](ONBOARDING.md) para crearla con `database/schema.sql`).
- Alternativa sin `.env`: también puedes definir las variables directamente en la sesión de PowerShell, aunque esto solo dura mientras la terminal esté abierta:

  ```powershell
  $env:DB_HOST="localhost"
  $env:DB_USER="root"
  $env:DB_PASSWORD="tu_contrasena_de_mysql"
  $env:DB_NAME="noreste_grill"
  ```

## Ejecutar la aplicación

```powershell
python -m backend.test_app
```

La aplicación inicia en `http://127.0.0.1:5000`.

## Versiones

Ver [VERSIONES.md](VERSIONES.md) para las herramientas, versiones, pasos de instalación y la razón por la que se usaron esas versiones.

## Onboarding

Ver [ONBOARDING.md](ONBOARDING.md) para la guía de instalación local, estructura del proyecto, roles, notas de base de datos y módulos principales.
