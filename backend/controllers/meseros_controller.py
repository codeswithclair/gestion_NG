from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import meseros_service

meseros_bp = Blueprint("meseros_bp", __name__)

CALIFICACION_SCHEMA = {
    "type": "object",
    "properties": {"calificacion": {"type": "number", "minimum": 0, "maximum": 10}},
}

TURNO_SCHEMA = {
    "type": "object",
    "properties": {"turno": {"type": "string"}},
}

OBSERVACION_SCHEMA = {
    "type": "object",
    "required": ["observacion"],
    "properties": {"observacion": {"type": "string"}},
}

PROMO_SCHEMA = {
    "type": "object",
    "required": ["id_promocion"],
    "properties": {
        "id_promocion": {"type": "integer"},
        "cantidad": {"type": "integer", "minimum": 1, "default": 1},
    },
}

MESERO_RESUMEN_SCHEMA = {
    "type": "object",
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre": {"type": "string"},
        "turno": {"type": "string"},
        "observacion": {"type": "string"},
        "calificacion": {"type": "number"},
        "mesas_atendidas": {"type": "integer"},
        "promedio": {"type": "number"},
        "promos": {"type": "integer"},
        "mesas_asignadas": {"type": "integer"},
        "ranking": {"type": "integer"},
        "mesas": {"type": "array", "items": {"type": "integer"}},
    },
}

MESERO_DETALLE_SCHEMA = {
    "type": "object",
    "properties": {
        **MESERO_RESUMEN_SCHEMA["properties"],
        "ranking": {"type": "string", "description": '"--" si no aplica, o el número de posición'},
    },
}

DETALLE_PROMO_SCHEMA = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "cantidad": {"type": "integer"},
    },
}

PROMOCION_SELECT_SCHEMA = {
    "type": "object",
    "properties": {
        "id_promocion": {"type": "integer"},
        "nombre": {"type": "string"},
    },
}


@meseros_bp.route("/personal")
def vista_gestion_meseros():
    return render_template("personal.html")


@meseros_bp.route("/rendimiento_mesero")
def vista_rendimiento_mesero():
    return render_template("rendimiento_mesero.html")


@meseros_bp.route("/api/meseros", methods=["GET"])
@doc(response=array_of(MESERO_RESUMEN_SCHEMA))
def obtener_meseros():
    return jsonify(meseros_service.listar_meseros())


@meseros_bp.route("/api/meseros/<int:no_empleado>", methods=["GET"])
@doc(response=MESERO_DETALLE_SCHEMA)
def obtener_mesero_individual(no_empleado):
    return jsonify(meseros_service.obtener_mesero(no_empleado))


@meseros_bp.route("/api/meseros/<int:no_empleado>/detalle-promos", methods=["GET"])
@doc(response=array_of(DETALLE_PROMO_SCHEMA))
def detalle_promos_mesero(no_empleado):
    return jsonify(meseros_service.detalle_promos(no_empleado))


@meseros_bp.route("/api/meseros/<int:no_empleado>/calificacion", methods=["PUT"])
@doc(body=CALIFICACION_SCHEMA, response=OK_RESPONSE)
def actualizar_calificacion(no_empleado):
    resultado = meseros_service.actualizar_calificacion(no_empleado, request.get_json())
    return jsonify(resultado)


@meseros_bp.route("/api/meseros/<int:no_empleado>/turno", methods=["PUT"])
@doc(body=TURNO_SCHEMA, response=OK_RESPONSE)
def actualizar_turno(no_empleado):
    resultado = meseros_service.actualizar_turno(no_empleado, request.get_json())
    return jsonify(resultado)


@meseros_bp.route("/api/meseros/<int:no_empleado>/observacion", methods=["PUT"])
@doc(body=OBSERVACION_SCHEMA, response=OK_RESPONSE)
def actualizar_observacion(no_empleado):
    resultado = meseros_service.actualizar_observacion(no_empleado, request.get_json())
    return jsonify(resultado)


@meseros_bp.route("/api/meseros/<int:no_empleado>/observacion", methods=["DELETE"])
@doc(response=OK_RESPONSE)
def eliminar_observacion(no_empleado):
    resultado = meseros_service.eliminar_observacion(no_empleado)
    return jsonify(resultado)


@meseros_bp.route("/api/meseros/<int:no_empleado>/promo", methods=["POST"])
@doc(body=PROMO_SCHEMA, response=OK_RESPONSE)
def registrar_promo_mesero(no_empleado):
    resultado = meseros_service.registrar_promo(no_empleado, request.get_json())
    return jsonify(resultado)


@meseros_bp.route("/api/promociones-select", methods=["GET"])
@doc(response=array_of(PROMOCION_SELECT_SCHEMA))
def promociones_para_select():
    return jsonify(meseros_service.listar_promociones_select())
