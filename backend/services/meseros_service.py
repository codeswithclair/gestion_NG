from backend.errors import ServiceError
from backend.repositories import meseros_repository


def _calcular_rankings(meseros):
    ordenados = sorted(
        meseros,
        key=lambda x: (
            float(x.get("calificacion") or 0),
            int(x.get("promos") or 0),
            int(x.get("mesas_atendidas") or 0),
            -float(x.get("promedio") or 999999),
        ),
        reverse=True,
    )

    for index, mesero_rank in enumerate(ordenados, start=1):
        for m in meseros:
            if m["no_empleado"] == mesero_rank["no_empleado"]:
                m["ranking"] = index
                break

    return meseros


def listar_meseros():
    meseros = _calcular_rankings(meseros_repository.fetch_resumen_meseros())

    for m in meseros:
        m["mesas"] = meseros_repository.fetch_mesas_de_mesero(m["no_empleado"])

    return meseros


def obtener_mesero(no_empleado):
    mesero = meseros_repository.fetch_resumen_mesero(no_empleado)
    if not mesero:
        raise ServiceError("Mesero no encontrado", 404)

    todos = _calcular_rankings(meseros_repository.fetch_resumen_para_ranking())

    mesero["ranking"] = "--"
    for m in todos:
        if m["no_empleado"] == no_empleado:
            mesero["ranking"] = m["ranking"]
            break

    mesero["mesas"] = meseros_repository.fetch_mesas_de_mesero(no_empleado)

    return mesero


def detalle_promos(no_empleado):
    return meseros_repository.fetch_detalle_promos(no_empleado)


def actualizar_calificacion(no_empleado, data):
    calificacion = float(data.get("calificacion", 0))
    calificacion = max(0, min(10, calificacion))

    id_gestion = meseros_repository.ensure_gestion_general(no_empleado)
    meseros_repository.update_calificacion(id_gestion, calificacion)

    return {"ok": True, "message": "Calificación actualizada"}


def actualizar_turno(no_empleado, data):
    id_gestion = meseros_repository.ensure_gestion_general(no_empleado)
    meseros_repository.update_turno(id_gestion, data.get("turno"))

    return {"ok": True, "message": "Turno actualizado"}


def actualizar_observacion(no_empleado, data):
    nueva_observacion = data.get("observacion", "").strip()
    if not nueva_observacion:
        raise ServiceError("La observación no puede estar vacía", 400)

    id_gestion = meseros_repository.ensure_gestion_general(no_empleado)
    observacion_actual = meseros_repository.get_observacion(id_gestion)

    if observacion_actual:
        observacion_final = observacion_actual + "\n- " + nueva_observacion
    else:
        observacion_final = "- " + nueva_observacion

    meseros_repository.set_observacion(id_gestion, observacion_final)

    return {"ok": True, "message": "Observación agregada correctamente"}


def eliminar_observacion(no_empleado):
    id_gestion = meseros_repository.ensure_gestion_general(no_empleado)
    meseros_repository.set_observacion(id_gestion, "")

    return {"ok": True, "message": "Observación eliminada correctamente"}


def registrar_promo(no_empleado, data):
    id_promocion = data.get("id_promocion")
    cantidad = int(data.get("cantidad", 1))

    if not id_promocion:
        raise ServiceError("Falta seleccionar promoción", 400)

    if cantidad <= 0:
        raise ServiceError("La cantidad debe ser mayor a cero", 400)

    id_gestion = meseros_repository.ensure_gestion_general(no_empleado)
    existe = meseros_repository.find_promo_gestion(id_promocion, id_gestion)

    if existe:
        meseros_repository.incrementar_promo_gestion(id_promocion, id_gestion, cantidad)
    else:
        meseros_repository.insertar_promo_gestion(id_promocion, id_gestion, cantidad)

    return {"ok": True, "message": "Promoción aplicada registrada correctamente"}


def listar_promociones_select():
    return meseros_repository.fetch_promociones_select()
