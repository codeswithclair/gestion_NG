from datetime import datetime

from backend.errors import ServiceError
from backend.repositories import mesas_repository


def _formatear(mesa):
    if mesa["hora_inicio"]:
        mesa["hora_inicio"] = mesa["hora_inicio"].strftime("%Y-%m-%d %H:%M:%S")
    if mesa["segundos_transcurridos"] is None:
        mesa["segundos_transcurridos"] = 0
    return mesa


def listar_mesas():
    return [_formatear(m) for m in mesas_repository.fetch_all()]


def actualizar_mesa(id_mesa, data):
    nuevo_estado = data.get("estado")
    nombre_cliente = data.get("nombre_cliente")
    no_personas = data.get("no_personas")
    nuevo_no_empleado = data.get("no_empleado")
    razon_retraso = data.get("razon_retraso")
    comentario_retraso = data.get("comentario_retraso")

    if nuevo_no_empleado == "":
        nuevo_no_empleado = None

    mesa_anterior = mesas_repository.get_by_id(id_mesa)
    if not mesa_anterior:
        raise ServiceError("Mesa no encontrada", 404)

    empleado_anterior = mesa_anterior.get("no_empleado")
    hora_inicio_anterior = mesa_anterior.get("hora_inicio")

    # Cuando una mesa ocupada con mesero pasa a libre,
    # se registra como mesa atendida en Gestion_de_meseros.
    if nuevo_estado == "libre" and empleado_anterior and hora_inicio_anterior:
        minutos_servicio = int((datetime.now() - hora_inicio_anterior).total_seconds() // 60)
        mesas_repository.liberar_y_registrar_atendida(id_mesa, empleado_anterior, minutos_servicio)
        return {"ok": True, "message": "Mesa liberada y registrada como atendida"}

    if nuevo_estado == "ocupada":
        mesas_repository.ocupar(id_mesa, nombre_cliente, no_personas, nuevo_no_empleado, razon_retraso, comentario_retraso)
    elif nuevo_estado == "limpieza":
        mesas_repository.poner_en_limpieza(id_mesa, razon_retraso, comentario_retraso)
    elif nuevo_estado == "libre":
        mesas_repository.liberar_simple(id_mesa)
    else:
        mesas_repository.set_estado_generico(id_mesa, nuevo_estado)

    return {"ok": True, "message": "Mesa actualizada correctamente"}


def guardar_retraso(id_mesa, data):
    mesas_repository.guardar_retraso(
        id_mesa,
        data.get("razon_retraso"),
        data.get("comentario_retraso", ""),
    )
    return {"ok": True, "message": "Razón del retraso guardada"}


def listar_meseros_disponibles():
    return mesas_repository.fetch_meseros_disponibles()
