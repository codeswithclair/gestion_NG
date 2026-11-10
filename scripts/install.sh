#!/usr/bin/env bash
# install.sh - instala y configura Noreste Grill en Debian/Ubuntu (o WSL).
#
# Pasos:
#   1. Instala paquetes del sistema (Python, venv, MariaDB).
#   2. Crea el entorno virtual e instala requirements.txt.
#   3. Crea el archivo .env (pide la password de la base de datos).
#   4. Crea la base de datos y el usuario de la aplicacion.
#   5. Carga database/schema.sql solo si la base esta vacia.
#
# Es seguro ejecutarlo varias veces: no pisa el .env ni los datos existentes.
# Uso: ./scripts/install.sh

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
cd "$PROJECT_DIR"

command -v apt-get >/dev/null || die "Este script requiere apt (Debian/Ubuntu)."

# ---------------------------------------------------------------- 1. Paquetes
info "[1/5] Instalando paquetes del sistema (pide sudo)..."
sudo apt-get update -qq
sudo apt-get install -y python3 python3-venv python3-pip mariadb-server
ok "Paquetes instalados."

# ---------------------------------------------------------------- 2. Venv
info "[2/5] Preparando entorno virtual..."
# Un venv copiado desde Windows (tiene Scripts/ en vez de bin/) no sirve: se recrea.
if [ ! -f venv/bin/activate ]; then
    rm -rf venv
    python3 -m venv venv
fi
venv/bin/pip install --quiet --upgrade pip
venv/bin/pip install --quiet -r requirements.txt
ok "Dependencias de Python instaladas."

# ---------------------------------------------------------------- 3. .env
info "[3/5] Configurando .env..."
if [ ! -f "$ENV_FILE" ]; then
    read -r -s -p "Elige una password para el usuario de BD 'noreste_app': " NEW_PASS
    echo
    [ -n "$NEW_PASS" ] || die "La password no puede estar vacia."
    printf '%s\n' \
        "DB_HOST=localhost" \
        "DB_NAME=noreste_grill" \
        "DB_USER=noreste_app" \
        "DB_PASSWORD=$NEW_PASS" > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    ok ".env creado."
else
    warn ".env ya existe, se conserva."
    [ "$(get_env DB_HOST)" = "localhost" ] || \
        warn "DB_HOST no es 'localhost' en tu .env; para correr sin Docker debe serlo."
fi

load_db_config
[ -n "$DB_PASSWORD" ] || die "DB_PASSWORD esta vacio en .env."
# Las comillas simples y las diagonales rompen el SQL de abajo.
case "$DB_PASSWORD" in
    *"'"*|*"\\"*) die "La password no puede contener ' ni \\ (cambiala en .env)." ;;
esac

# ---------------------------------------------------------------- 4. Base de datos
info "[4/5] Creando base de datos y usuario..."
sudo service mariadb start
sudo mariadb <<SQL
CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
ALTER USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON \`$DB_NAME\`.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL
ok "Base '$DB_NAME' y usuario '$DB_USER' listos."

# ---------------------------------------------------------------- 5. Esquema
info "[5/5] Cargando esquema..."
TABLES="$(sudo mariadb -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")"
if [ "$TABLES" -eq 0 ]; then
    sudo mariadb "$DB_NAME" < database/schema.sql > /dev/null
    ok "schema.sql cargado."
else
    warn "La base ya tiene $TABLES tablas; no se vuelve a cargar schema.sql."
fi

echo
ok "Instalacion terminada. Inicia la app con: ./scripts/run.sh"
