#!/usr/bin/env bash
# backup.sh - respalda la base de datos y los archivos del proyecto.
#
# Genera UN archivo: noreste_grill_backup_AAAAMMDD_HHMMSS.tar.gz que contiene
#   - el codigo del proyecto (sin venv, .git, logs ni respaldos anteriores)
#   - un volcado SQL de la base de datos (noreste_grill.sql)
#
# Uso:
#   ./scripts/backup.sh                  # guarda en ./backups
#   ./scripts/backup.sh /ruta/destino    # guarda en otra carpeta
#   KEEP=14 ./scripts/backup.sh          # conserva los 14 respaldos mas nuevos (default 7)
#
# Se puede programar con cron, por ejemplo todos los dias a las 2:00:
#   0 2 * * * /ruta/al/proyecto/scripts/backup.sh
#
# Para restaurar la base:
#   tar -xzf respaldo.tar.gz noreste_grill.sql
#   sudo mariadb noreste_grill < noreste_grill.sql

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

DEST_DIR="${1:-$DEFAULT_BACKUP_DIR}"
KEEP="${KEEP:-7}"

load_db_config
[ -n "$DB_PASSWORD" ] || die "No se encontro DB_PASSWORD en .env."
command -v mariadb-dump >/dev/null || command -v mysqldump >/dev/null \
    || die "No se encontro mariadb-dump/mysqldump."
DUMP_CMD="$(command -v mariadb-dump || command -v mysqldump)"

mkdir -p "$DEST_DIR"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
ARCHIVE="$DEST_DIR/noreste_grill_backup_${TIMESTAMP}.tar.gz"

# Carpeta temporal para el volcado; se borra sola al terminar (trap EXIT),
# incluso si el script falla a la mitad.
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

info "Volcando la base de datos '$DB_NAME'..."
# MYSQL_PWD evita poner la password en la linea de comandos (se veria en "ps").
MYSQL_PWD="$DB_PASSWORD" "$DUMP_CMD" -u "$DB_USER" --single-transaction \
    "$DB_NAME" > "$TMP_DIR/${DB_NAME}.sql"

info "Comprimiendo proyecto + base de datos..."
tar -czf "$ARCHIVE" \
    --exclude=./venv --exclude=./.git --exclude=./logs --exclude=./backups \
    --exclude=__pycache__ --exclude=./.app.pid \
    -C "$PROJECT_DIR" . \
    -C "$TMP_DIR" "${DB_NAME}.sql"
chmod 600 "$ARCHIVE"   # incluye .env con la password: solo el dueno puede leerlo
ok "Respaldo creado: $ARCHIVE ($(du -h "$ARCHIVE" | cut -f1))"

# Rotacion: borra los respaldos mas viejos y deja los KEEP mas recientes.
mapfile -t OLD < <(ls -1t "$DEST_DIR"/noreste_grill_backup_*.tar.gz 2>/dev/null | tail -n +"$((KEEP + 1))")
if [ "${#OLD[@]}" -gt 0 ]; then
    rm -f -- "${OLD[@]}"
    info "Se eliminaron ${#OLD[@]} respaldo(s) antiguo(s)."
fi
