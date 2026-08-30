# Versiones y herramientas utilizadas

Este documento describe las versiones principales usadas en el proyecto, como instalarlas y por que se eligieron.

## Resumen de versiones

| Herramienta | Version usada | Uso en el proyecto |
| --- | --- | --- |
| Python | 3.14.5 | Lenguaje principal del backend |
| Flask | 3.1.3 | Framework web para rutas, APIs y templates |
| MySQL | Version local instalada en el equipo | Base de datos del sistema |
| mysql-connector-python | 9.6.0 | Conexion entre Python y MySQL |
| Waitress | 3.0.2 | Servidor WSGI para correr Flask en modo mas cercano a produccion |

## Python 3.14.5

Python se usa como lenguaje principal del proyecto. Toda la logica del backend esta escrita en archivos `.py` dentro de la carpeta `backend`, por ejemplo `backend/test_app.py`, `backend/auth.py`, `backend/usuarios.py`, `backend/reservaciones.py` y `backend/meseros.py`.

### Como instalar Python

1. Entrar a la pagina oficial: <https://www.python.org/downloads/>
2. Descargar Python para Windows.
3. Durante la instalacion, activar la opcion **Add Python to PATH**.
4. Verificar la instalacion con:

```powershell
python --version
```

En este proyecto se uso:

```text
Python 3.14.5
```

### Por que se uso esta version

Se uso Python 3.14.5 porque era la version instalada y disponible en el ambiente donde se comenzo a desarrollar el proyecto. Mantener esta version ayuda a que el proyecto siga funcionando igual que durante el desarrollo original.

## Flask 3.1.3

Flask es el framework web usado para crear la aplicacion. Permite definir rutas, registrar blueprints, responder peticiones desde JavaScript y renderizar archivos HTML desde la carpeta `templates`.

### Como instalar Flask

Flask se instala desde el archivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

Tambien se puede instalar directamente con:

```powershell
pip install Flask==3.1.3
```

### Por que se uso esta version

Se uso Flask 3.1.3 porque fue la version instalada en el entorno virtual del proyecto cuando se desarrollo la aplicacion. Es una version actual y compatible con la estructura usada en el sistema, incluyendo blueprints, templates y respuestas JSON.

## MySQL

MySQL se usa como sistema gestor de base de datos. El proyecto se conecta a una base llamada:

```text
noreste_grill
```

La conexion se configura desde `backend/db.py` usando variables de entorno:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

### Como instalar MySQL

1. Entrar a la pagina oficial: <https://dev.mysql.com/downloads/installer/>
2. Descargar **MySQL Installer for Windows**.
3. Instalar **MySQL Server**.
4. Configurar un usuario, normalmente `root`, y una contrasena.
5. Crear la base de datos `noreste_grill`.

Para verificar la version, se puede usar MySQL Workbench o ejecutar:

```powershell
mysql --version
```

Nota: en este equipo el comando `mysql` no esta disponible desde PowerShell, por eso no se pudo detectar automaticamente la version exacta del servidor MySQL.

### Por que se uso MySQL

Se uso MySQL porque era la base de datos disponible al iniciar el proyecto y porque funciona bien para guardar informacion estructurada como usuarios, roles, reservaciones, mesas, promociones y lista de espera.

## mysql-connector-python 9.6.0

`mysql-connector-python` permite que el codigo Python se conecte a MySQL.

### Como instalarlo

Se instala junto con las demas dependencias:

```powershell
pip install -r requirements.txt
```

O de forma individual:

```powershell
pip install mysql-connector-python==9.6.0
```

### Por que se uso esta version

Se uso la version 9.6.0 porque era la version instalada en el entorno virtual al momento de preparar el proyecto. Mantenerla fija en `requirements.txt` evita cambios inesperados al instalar el proyecto en otra computadora.

## Waitress 3.0.2

Waitress es un servidor WSGI para correr aplicaciones Flask. Aunque durante desarrollo se puede usar:

```powershell
python -m backend.test_app
```

Waitress es util cuando se quiere ejecutar la aplicacion de una forma mas parecida a produccion.

### Como instalar Waitress

Se instala desde `requirements.txt`:

```powershell
pip install -r requirements.txt
```

O directamente:

```powershell
pip install waitress==3.0.2
```

### Por que se uso esta version

Se mantuvo Waitress 3.0.2 porque ya estaba instalado en el entorno del proyecto. Sirve como opcion para ejecutar Flask sin depender del servidor de desarrollo integrado.

## Instalacion completa del proyecto

Desde la carpeta del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Despues se configuran las variables de entorno para la base de datos:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="tu_contrasena"
$env:DB_NAME="noreste_grill"
```

Finalmente, se ejecuta la aplicacion:

```powershell
python -m backend.test_app
```

## Nota sobre las versiones

Las versiones se dejaron fijas porque fueron las utilizadas durante el desarrollo del proyecto. Esto ayuda a que otra persona pueda instalar el sistema con un ambiente lo mas parecido posible al original y reduce errores por diferencias entre versiones.
