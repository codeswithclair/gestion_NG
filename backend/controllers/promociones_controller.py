from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import promociones_service

promociones_bp = Blueprint("promociones_bp", __name__)

PROMOCION_SCHEMA = {
    "type": "object",
    "required": ["no_empleado", "nombre", "descripcion", "vigencia_inicio", "vigencia_fin", "estado", "dias_vigentes"],
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre": {"type": "string"},
        "descripcion": {"type": "string"},
        "condiciones": {"type": "string"},
        "vigencia_inicio": {"type": "string", "format": "date"},
        "vigencia_fin": {"type": "string", "format": "date"},
        "estado": {"type": "integer", "enum": [0, 1]},
        "ocasion": {"type": "string"},
        "dias_vigentes": {"type": "string"},
    },
}

ESTADO_SCHEMA = {
    "type": "object",
    "required": ["estado"],
    "properties": {"estado": {"type": "integer", "enum": [0, 1]}},
}

PROMOCION_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "id_promocion": {"type": "integer"},
        "no_empleado": {"type": "integer"},
        "nombre": {"type": "string"},
        "descripcion": {"type": "string"},
        "condiciones": {"type": "string"},
        "vigencia_inicio": {"type": "string", "format": "date"},
        "vigencia_fin": {"type": "string", "format": "date"},
        "estado": {"type": "boolean"},
        "ocasion": {"type": "string"},
        "dias_vigentes": {"type": "string"},
    },
}

CREAR_PROMOCION_RESPONSE = {
    "type": "object",
    "properties": {
        "ok": {"type": "boolean"},
        "message": {"type": "string"},
        "id_promocion": {"type": "integer"},
    },
}


@promociones_bp.route("/gestion_promociones")
def vista_gestion_promociones():
    return render_template("gestion_promociones.html")


@promociones_bp.route("/promociones_vigentes")
def vista_promociones_vigentes():
    return render_template("promociones_vigentes.html")


@promociones_bp.route("/api/promociones", methods=["GET"])
@doc(response=array_of(PROMOCION_ITEM_SCHEMA))
def obtener_promociones():
    return jsonify(promociones_service.listar_promociones())


@promociones_bp.route("/api/promociones-vigentes", methods=["GET"])
@doc(response=array_of(PROMOCION_ITEM_SCHEMA))
def obtener_promociones_vigentes():
    return jsonify(promociones_service.listar_vigentes())


@promociones_bp.route("/api/promociones", methods=["POST"])
@doc(body=PROMOCION_SCHEMA, response=CREAR_PROMOCION_RESPONSE)
def crear_promocion():
    resultado = promociones_service.crear_promocion(request.get_json())
    return jsonify(resultado), 201


@promociones_bp.route("/api/promociones/<int:id_promocion>", methods=["PUT"])
@doc(body=PROMOCION_SCHEMA, response=OK_RESPONSE)
def actualizar_promocion(id_promocion):
    resultado = promociones_service.actualizar_promocion(id_promocion, request.get_json())
    return jsonify(resultado)


@promociones_bp.route("/api/promociones/<int:id_promocion>/estado", methods=["PUT"])
@doc(body=ESTADO_SCHEMA, response=OK_RESPONSE)
def cambiar_estado_promocion(id_promocion):
    resultado = promociones_service.cambiar_estado_promocion(id_promocion, request.get_json())
    return jsonify(resultado)


@promociones_bp.route("/api/promociones/<int:id_promocion>", methods=["DELETE"])
@doc(response=OK_RESPONSE)
def eliminar_promocion(id_promocion):
    resultado = promociones_service.eliminar_promocion(id_promocion)
    return jsonify(resultado)
