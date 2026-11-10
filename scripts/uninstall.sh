#!/usr/bin/env bash
# uninstall.sh - elimina el proyecto Noreste Grill de esta maquina.
#
# Pregunta paso a paso y NO continua sin confirmacion:
#   1. Detiene la app.
#   2. (opcional) Hace un respaldo antes de borrar.
#   3. (opcional) Elimina la base de datos y el usuario de MariaDB.
#   4. (opcional) Elimina la carpeta completa del proyecto.
#
# No desinstala MariaDB/Python (otros programas podrian usarlos). Si tambien
# quieres quitar MariaDB:  sudo apt remove --purge mariadb-server
#
# Uso: ./scripts/uninstall.sh

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

load_db_config

# Salvaguarda: nunca borrar rutas peligrosas por un error de calculo.
case "$PROJECT_DIR" in
    ""|"/"|"$HOME"|"/home"|"/usr"|"/etc") die "Ruta de proyecto insegura: '$PROJECT_DIR'" ;;
esac

echo "Se va a desinstalar el proyecto ubicado en: $PROJECT_DIR"
echo "Base de datos: $DB_NAME   Usuario de BD: $DB_USER"
echo
confirm "Seguro que quieres continuar?" || { info "Cancelado."; exit 0; }

# 1. Detener la app
"$SCRIPTS_DIR/run.sh" stop

# 2. Respaldo previo
if confirm "Hacer un respaldo antes de borrar? (se guarda en ~/respaldos_noreste_grill)"; then
    "$SCRIPTS_DIR/backup.sh" "$HOME/respaldos_noreste_grill"
fi

# 3. Base de datos
if confirm "Eliminar la base de datos '$DB_NAME' y el usuario '$DB_USER'? (se pierden los datos)"; then
    sudo service mariadb start
    sudo mariadb <<SQL
DROP DATABASE IF EXISTS \`$DB_NAME\`;
DROP USER IF EXISTS '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
SQL
    ok "Base de datos y usuario eliminados."
else
    info "Base de datos conservada."
fi

# 4. Archivos del proyecto
if confirm "Eliminar la carpeta del proyecto ($PROJECT_DIR)?"; then
    read -r -p "Escribe ELIMINAR en mayusculas para confirmar: " WORD
    [ "$WORD" = "ELIMINAR" ] || { info "Cancelado, no se borraron archivos."; exit 0; }
    # Nos salimos de la carpeta antes de borrarla; rm va al final del script.
    cd "$HOME"
    rm -rf -- "$PROJECT_DIR"
    ok "Proyecto eliminado."
else
    info "Archivos conservados."
fi
