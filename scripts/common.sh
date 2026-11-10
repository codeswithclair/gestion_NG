#!/usr/bin/env bash
# common.sh - variables y funciones compartidas por los demas scripts.
# No se ejecuta directamente: los otros scripts lo cargan con "source".

# Rutas (se calculan a partir de la ubicacion de este archivo, asi los scripts
# funcionan sin importar desde que carpeta se invoquen).
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPTS_DIR")"
ENV_FILE="$PROJECT_DIR/.env"
PID_FILE="$PROJECT_DIR/.app.pid"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/app.log"
DEFAULT_BACKUP_DIR="$PROJECT_DIR/backups"

# Datos de la aplicacion
APP_MODULE="backend.test_app"
APP_PORT=5000

# Mensajes con color
info() { printf '\033[1;34m[INFO]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m[ OK ]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[WARN]\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m[ERROR]\033[0m %s\n' "$*" >&2; exit 1; }

# get_env CLAVE -> imprime el valor de CLAVE en el .env (vacio si no existe).
# Se lee con grep en lugar de "source .env" para no ejecutar nada del archivo.
get_env() {
    [ -f "$ENV_FILE" ] || return 0
    { grep -E "^$1=" "$ENV_FILE" | head -n1 | cut -d= -f2-; } || true
}

# load_db_config -> deja DB_NAME, DB_USER y DB_PASSWORD listos para usar.
load_db_config() {
    DB_NAME="$(get_env DB_NAME)";         DB_NAME="${DB_NAME:-noreste_grill}"
    DB_USER="$(get_env DB_USER)";         DB_USER="${DB_USER:-noreste_app}"
    DB_PASSWORD="$(get_env DB_PASSWORD)"; DB_PASSWORD="${DB_PASSWORD:-}"
}

# confirm "pregunta" -> devuelve 0 solo si el usuario escribe "s" o "si".
confirm() {
    local answer
    read -r -p "$1 [s/N]: " answer
    [[ "${answer,,}" == "s" || "${answer,,}" == "si" ]]
}
