from flask import Blueprint, jsonify, render_template

from backend.openapi_spec import doc
from backend.services import dashboard_jefepiso_service

dashboard_jefepiso_bp = Blueprint("dashboard_jefepiso_bp", __name__)

DASHBOARD_JEFEPISO_RESPONSE = {
    "type": "object",
    "properties": {
        "mesas_servicio": {"type": "integer"},
        "retrasos_hoy": {"type": "integer"},
        "meseros_turno": {"type": "integer"},
        "mesas_asignadas": {"type": "integer"},
        "destacado": {
            "type": "object",
            "nullable": True,
            "properties": {
                "nombre": {"type": "string"},
                "calificacion": {"type": "number"},
            },
        },
        "retrasos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id_mesa": {"type": "integer"},
                    "razon_retraso": {"type": "string"},
                },
            },
        },
    },
}


@dashboard_jefepiso_bp.route("/jefepiso")
def jefepiso_dashboard():
    return render_template("jefepiso_dashboard.html")


@dashboard_jefepiso_bp.route("/api/dashboard/jefepiso")
@doc(response=DASHBOARD_JEFEPISO_RESPONSE)
def api_dashboard_jefepiso():
    return jsonify(dashboard_jefepiso_service.obtener_dashboard())
