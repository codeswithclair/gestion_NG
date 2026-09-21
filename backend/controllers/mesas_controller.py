from flask import Blueprint, jsonify, render_template, request, send_file

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

PROMEDIO_ATENCION_SCHEMA = {
    "type": "object",
    "properties": {
        "promedio_minutos": {"type": "number"},
        "mesas_atendidas": {"type": "integer"},
    },
}

MOTIVO_RETRASO_SCHEMA = {
    "type": "object",
    "properties": {
        "motivo": {"type": "string", "nullable": True},
        "total": {"type": "integer"},
    },
}

RESUMEN_REPORTE_SCHEMA = {
    "type": "object",
    "properties": {
        "fecha_inicio": {"type": "string", "format": "date", "nullable": True},
        "fecha_fin": {"type": "string", "format": "date", "nullable": True},
        "promedio_minutos": {"type": "number"},
        "mesas_atendidas": {"type": "integer"},
        "motivo_mas_frecuente": {"type": "string", "nullable": True},
        "motivo_total": {"type": "integer"},
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


@mesas_bp.route("/api/mesas/reportes/promedio-atencion", methods=["GET"])
@doc(response=PROMEDIO_ATENCION_SCHEMA, summary="Promedio de tiempo de atención por mesa, día o rango de fechas")
def obtener_promedio_atencion():
    return jsonify(mesas_service.obtener_promedio_atencion(request.args))


@mesas_bp.route("/api/mesas/reportes/motivo-retraso-frecuente", methods=["GET"])
@doc(response=MOTIVO_RETRASO_SCHEMA, summary="Motivo de retraso más frecuente en un rango de fechas")
def obtener_motivo_retraso_frecuente():
    return jsonify(mesas_service.obtener_motivo_retraso_frecuente(request.args))


@mesas_bp.route("/api/mesas/reportes/resumen", methods=["GET"])
@doc(response=RESUMEN_REPORTE_SCHEMA, summary="Resumen para previsualizar antes de descargar el reporte PDF")
def obtener_resumen_reporte():
    return jsonify(mesas_service.obtener_resumen_reporte(request.args))


@mesas_bp.route("/api/mesas/reportes/pdf", methods=["GET"])
@doc(summary="Descarga el reporte de mesas y retrasos en PDF")
def descargar_reporte_pdf():
    buffer = mesas_service.generar_reporte_pdf(request.args)
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="reporte_mesas_retrasos.pdf",
    )
