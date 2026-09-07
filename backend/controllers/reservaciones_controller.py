from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import reservaciones_service

reservaciones_bp = Blueprint("reservaciones_bp", __name__)

RESERVACION_SCHEMA = {
    "type": "object",
    "required": ["nombre_cliente", "telefono", "fecha", "hora", "no_personas", "estado"],
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre_cliente": {"type": "string"},
        "apellido_cliente": {"type": "string"},
        "telefono": {"type": "string", "description": "10 dígitos"},
        "fecha": {"type": "string", "format": "date", "example": "2026-09-10"},
        "hora": {"type": "string", "format": "time", "example": "20:30:00"},
        "no_personas": {"type": "integer"},
        "estado": {"type": "string"},
        "comentarios": {"type": "string"},
    },
}

RESERVACION_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "id_reservacion": {"type": "integer"},
        "no_empleado": {"type": "integer"},
        "nombre_cliente": {"type": "string"},
        "apellido_cliente": {"type": "string"},
        "telefono": {"type": "string"},
        "fecha": {"type": "string", "format": "date"},
        "hora": {"type": "string", "example": "20:30:00"},
        "fecha_registro": {"type": "string", "format": "date-time"},
        "no_personas": {"type": "integer"},
        "estado": {"type": "string"},
        "comentarios": {"type": "string"},
    },
}

CREAR_RESERVACION_RESPONSE = {
    "type": "object",
    "properties": {
        "ok": {"type": "boolean"},
        "message": {"type": "string"},
        "id_reservacion": {"type": "integer"},
    },
}


@reservaciones_bp.route("/reservaciones")
def vista_reservaciones():
    return render_template("reservaciones.html")


@reservaciones_bp.route("/api/reservaciones", methods=["GET"])
@doc(response=array_of(RESERVACION_ITEM_SCHEMA))
def obtener_reservaciones():
    return jsonify(reservaciones_service.listar_reservaciones())


@reservaciones_bp.route("/api/reservaciones", methods=["POST"])
@doc(body=RESERVACION_SCHEMA, response=CREAR_RESERVACION_RESPONSE)
def crear_reservacion():
    resultado = reservaciones_service.crear_reservacion(request.get_json())
    return jsonify(resultado), 201


@reservaciones_bp.route("/api/reservaciones/<int:id_reservacion>", methods=["PUT"])
@doc(body=RESERVACION_SCHEMA, response=OK_RESPONSE)
def actualizar_reservacion(id_reservacion):
    resultado = reservaciones_service.actualizar_reservacion(id_reservacion, request.get_json())
    return jsonify(resultado)


@reservaciones_bp.route("/api/reservaciones/<int:id_reservacion>", methods=["DELETE"])
@doc(response=OK_RESPONSE)
def eliminar_reservacion(id_reservacion):
    resultado = reservaciones_service.eliminar_reservacion(id_reservacion)
    return jsonify(resultado)
