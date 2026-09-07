from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import mesas_service

mesas_bp = Blueprint("mesas_bp", __name__)

MESA_UPDATE_SCHEMA = {
    "type": "object",
    "required": ["estado"],
    "properties": {
        "estado": {"type": "string", "enum": ["libre", "ocupada", "limpieza"]},
        "nombre_cliente": {"type": "string"},
        "no_personas": {"type": "integer"},
        "no_empleado": {"type": "integer"},
        "razon_retraso": {"type": "string"},
        "comentario_retraso": {"type": "string"},
    },
}

RETRASO_SCHEMA = {
    "type": "object",
    "properties": {
        "razon_retraso": {"type": "string"},
        "comentario_retraso": {"type": "string"},
    },
}

MESA_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "id_mesa": {"type": "integer"},
        "no_empleado": {"type": "integer", "nullable": True},
        "nombre_mesero": {"type": "string", "nullable": True},
        "estado": {"type": "string", "enum": ["libre", "ocupada", "limpieza"]},
        "nombre_cliente": {"type": "string", "nullable": True},
        "no_personas": {"type": "integer", "nullable": True},
        "hora_inicio": {"type": "string", "format": "date-time", "nullable": True},
        "razon_retraso": {"type": "string", "nullable": True},
        "comentario_retraso": {"type": "string", "nullable": True},
        "segundos_transcurridos": {"type": "integer"},
    },
}

MESERO_DISPONIBLE_SCHEMA = {
    "type": "object",
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre_completo": {"type": "string"},
    },
}


@mesas_bp.route("/estado_mesas")
def vista_estado_mesas():
    return render_template("estado_mesas.html")


@mesas_bp.route("/api/mesas", methods=["GET"])
@doc(response=array_of(MESA_ITEM_SCHEMA))
def obtener_mesas():
    return jsonify(mesas_service.listar_mesas())


@mesas_bp.route("/api/mesas/<int:id_mesa>", methods=["PUT"])
@doc(body=MESA_UPDATE_SCHEMA, response=OK_RESPONSE)
def actualizar_mesa(id_mesa):
    resultado = mesas_service.actualizar_mesa(id_mesa, request.get_json())
    return jsonify(resultado)


@mesas_bp.route("/api/mesas/<int:id_mesa>/retraso", methods=["PUT"])
@doc(body=RETRASO_SCHEMA, response=OK_RESPONSE)
def guardar_retraso(id_mesa):
    resultado = mesas_service.guardar_retraso(id_mesa, request.get_json())
    return jsonify(resultado)


@mesas_bp.route("/api/meseros-disponibles", methods=["GET"])
@doc(response=array_of(MESERO_DISPONIBLE_SCHEMA))
def obtener_meseros_disponibles():
    return jsonify(mesas_service.listar_meseros_disponibles())
