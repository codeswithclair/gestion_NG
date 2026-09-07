from mysql.connector import IntegrityError

from backend.repositories import promociones_repository


def _formatear(promocion):
    if promocion["vigencia_inicio"]:
        promocion["vigencia_inicio"] = promocion["vigencia_inicio"].strftime("%Y-%m-%d")
    if promocion["vigencia_fin"]:
        promocion["vigencia_fin"] = promocion["vigencia_fin"].strftime("%Y-%m-%d")
    promocion["estado"] = bool(promocion["estado"])
    return promocion


def listar_promociones():
    return [_formatear(p) for p in promociones_repository.fetch_all()]


def listar_vigentes():
    return [_formatear(p) for p in promociones_repository.fetch_vigentes()]


def crear_promocion(data):
    nuevo_id = promociones_repository.insert(
        data["no_empleado"],
        data["nombre"],
        data["descripcion"],
        data.get("condiciones", ""),
        data["vigencia_inicio"],
        data["vigencia_fin"],
        data["estado"],
        data.get("ocasion", ""),
        data["dias_vigentes"],
    )
    return {
        "ok": True,
        "message": "Promoción registrada correctamente",
        "id_promocion": nuevo_id,
    }


def actualizar_promocion(id_promocion, data):
    promociones_repository.update(
        id_promocion,
        data["nombre"],
        data["descripcion"],
        data.get("condiciones", ""),
        data["vigencia_inicio"],
        data["vigencia_fin"],
        data["estado"],
        data.get("ocasion", ""),
        data["dias_vigentes"],
    )
    return {"ok": True, "message": "Promoción actualizada correctamente"}


def cambiar_estado_promocion(id_promocion, data):
    promociones_repository.update_estado(id_promocion, data["estado"])
    return {"ok": True, "message": "Estado actualizado correctamente"}


def eliminar_promocion(id_promocion):
    try:
        promociones_repository.delete(id_promocion)
        message = "Promoción eliminada correctamente"
    except IntegrityError:
        promociones_repository.desactivar(id_promocion)
        message = "La promoción ya tenía registros aplicados, por eso se desactivó en lugar de eliminarse"

    return {"ok": True, "message": message}
