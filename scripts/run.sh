#!/usr/bin/env bash
# run.sh - inicia, detiene y consulta la aplicacion Flask.
#
# Uso:
#   ./scripts/run.sh            # = start: corre en segundo plano
#   ./scripts/run.sh start
#   ./scripts/run.sh stop
#   ./scripts/run.sh restart
#   ./scripts/run.sh status
#   ./scripts/run.sh logs       # sigue el log en vivo (Ctrl+C para salir)
#   ./scripts/run.sh fg         # corre en primer plano, viendo los logs aqui

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
cd "$PROJECT_DIR"

# Devuelve 0 si el PID guardado en .app.pid corresponde a un proceso vivo.
is_running() {
    [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

check_ready() {
    [ -x venv/bin/python ] || die "No existe venv/. Ejecuta primero ./scripts/install.sh"
    [ -f "$ENV_FILE" ]     || die "No existe .env. Ejecuta primero ./scripts/install.sh"
    # service es idempotente: si MariaDB ya esta corriendo no pasa nada.
    sudo service mariadb start > /dev/null
}

start() {
    if is_running; then
        warn "Ya esta corriendo (PID $(cat "$PID_FILE"))."
        return
    fi
    check_ready
    mkdir -p "$LOG_DIR"

    info "Iniciando Flask en segundo plano..."
    # setsid  -> proceso en su propio grupo: sobrevive al cerrar la terminal y
    #            permite detenerlo completo (Flask en modo debug crea un hijo).
    # nohup   -> ignora la senal de cierre de sesion.
    # >> 2>&1 -> stdout y stderr van al archivo de log en vez de la pantalla.
    setsid nohup venv/bin/python -m "$APP_MODULE" >> "$LOG_FILE" 2>&1 < /dev/null &
    echo $! > "$PID_FILE"

    sleep 2
    if is_running; then
        ok "App corriendo (PID $(cat "$PID_FILE")) en http://127.0.0.1:$APP_PORT"
        info "Logs: $LOG_FILE  (verlos con: ./scripts/run.sh logs)"
    else
        rm -f "$PID_FILE"
        die "La app no arranco. Revisa $LOG_FILE"
    fi
}

stop() {
    if ! is_running; then
        warn "La app no esta corriendo."
        rm -f "$PID_FILE"
        return
    fi
    local pid
    pid="$(cat "$PID_FILE")"
    # "kill -- -PID" manda la senal a todo el grupo (proceso padre y recargador).
    kill -- "-$pid" 2>/dev/null || kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    ok "App detenida."
}

status() {
    if is_running; then
        ok "Corriendo (PID $(cat "$PID_FILE")) en http://127.0.0.1:$APP_PORT"
    else
        warn "Detenida."
    fi
}

case "${1:-start}" in
    start)   start ;;
    stop)    stop ;;
    restart) stop; start ;;
    status)  status ;;
    logs)    [ -f "$LOG_FILE" ] || die "Aun no hay log."; tail -n 50 -f "$LOG_FILE" ;;
    fg)      check_ready; exec venv/bin/python -m "$APP_MODULE" ;;
    *)       echo "Uso: $0 {start|stop|restart|status|logs|fg}"; exit 1 ;;
esac
