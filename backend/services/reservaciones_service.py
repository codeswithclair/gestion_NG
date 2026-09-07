from datetime import datetime

from backend.errors import ServiceError
from backend.repositories import reservaciones_repository


def _validar_fecha_hora(fecha_str, hora_str):
    try:
        fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, "Formato de fecha u hora inválido"

    if fecha_hora < datetime.now():
        return False, "No se puede registrar una reservación en una fecha u hora que ya pasó"

    return True, ""


def _validar_reservacion(data):
    campos_obligatorios = ["nombre_cliente", "telefono", "fecha", "hora", "no_personas", "estado"]

    for campo in campos_obligatorios:
        if not data.get(campo):
            return False, "Completa todos los campos obligatorios."

    telefono = "".join(digito for digito in str(data["telefono"]) if digito.isdigit())
    if len(telefono) != 10:
        return False, "El telefono debe tener exactamente 10 digitos."

    data["telefono"] = telefono

    valido, mensaje = _validar_fecha_hora(data["fecha"], data["hora"])
    if not valido:
        return False, mensaje

    return True, ""


def _formatear(reservacion):
    if reservacion["fecha"]:
        reservacion["fecha"] = reservacion["fecha"].strftime("%Y-%m-%d")

    if reservacion["hora"]:
        total_seconds = int(reservacion["hora"].total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        reservacion["hora"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    if reservacion["fecha_registro"]:
        reservacion["fecha_registro"] = reservacion["fecha_registro"].strftime("%Y-%m-%d %H:%M:%S")

    return reservacion


def listar_reservaciones():
    return [_formatear(r) for r in reservaciones_repository.fetch_all()]


def crear_reservacion(data):
    valido, mensaje = _validar_reservacion(data)
    if not valido:
        raise ServiceError(mensaje, 400)

    nuevo_id = reservaciones_repository.insert(
        data["no_empleado"],
        data["nombre_cliente"],
        data.get("apellido_cliente", ""),
        data["telefono"],
        data["fecha"],
        data["hora"],
        data["no_personas"],
        data["estado"],
        data.get("comentarios", ""),
    )

    return {
        "ok": True,
        "message": "Reservación creada correctamente",
        "id_reservacion": nuevo_id,
    }


def actualizar_reservacion(id_reservacion, data):
    valido, mensaje = _validar_reservacion(data)
    if not valido:
        raise ServiceError(mensaje, 400)

    rowcount = reservaciones_repository.update(
        id_reservacion,
        data["nombre_cliente"],
        data.get("apellido_cliente", ""),
        data["telefono"],
        data["fecha"],
        data["hora"],
        data["no_personas"],
        data["estado"],
        data.get("comentarios", ""),
    )

    if rowcount == 0:
        raise ServiceError("Reservación no encontrada", 404)

    return {"ok": True, "message": "Reservación actualizada correctamente"}


def eliminar_reservacion(id_reservacion):
    rowcount = reservaciones_repository.delete(id_reservacion)

    if rowcount == 0:
        raise ServiceError("Reservación no encontrada", 404)

    return {"ok": True, "message": "Reservación eliminada correctamente"}
