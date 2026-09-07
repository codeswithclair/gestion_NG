from flask import Blueprint, jsonify, render_template

from backend.openapi_spec import doc
from backend.services import dashboard_gerente_service

dashboard_gerente_bp = Blueprint("dashboard_gerente_bp", __name__)

DASHBOARD_GERENTE_RESPONSE = {
    "type": "object",
    "properties": {
        "usuarios_activos": {"type": "integer"},
        "reservaciones_hoy": {"type": "integer"},
        "promociones_activas": {"type": "integer"},
        "rendimiento_promedio": {"type": "number"},
        "reservaciones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nombre_cliente": {"type": "string"},
                    "no_personas": {"type": "integer"},
                    "hora": {"type": "string"},
                    "estado": {"type": "string"},
                },
            },
        },
        "promociones": {
            "type": "array",
            "items": {"type": "object", "properties": {"nombre": {"type": "string"}}},
        },
        "mejores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "calificacion": {"type": "number"},
                },
            },
        },
    },
}


@dashboard_gerente_bp.route("/gerente")
def gerente_dashboard():
    return render_template("gerente_dashboard.html")


@dashboard_gerente_bp.route("/api/dashboard/gerente")
@doc(response=DASHBOARD_GERENTE_RESPONSE)
def api_dashboard_gerente():
    return jsonify(dashboard_gerente_service.obtener_dashboard())
