from flask import Blueprint, jsonify, render_template

from backend.openapi_spec import doc
from backend.services import dashboard_hostess_service

dashboard_hostess_bp = Blueprint("dashboard_hostess_bp", __name__)

DASHBOARD_HOSTESS_RESPONSE = {
    "type": "object",
    "properties": {
        "clientes_espera": {"type": "integer"},
        "mesas_ocupadas": {"type": "integer"},
        "mesas_libres": {"type": "integer"},
        "promedio_servicio": {"type": "number"},
        "promociones_vigentes": {"type": "integer"},
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
        "espera": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "no_personas": {"type": "integer"},
                },
            },
        },
    },
}


@dashboard_hostess_bp.route("/hostess")
def hostess_dashboard():
    return render_template("hostess_dashboard.html")


@dashboard_hostess_bp.route("/api/dashboard/hostess")
@doc(response=DASHBOARD_HOSTESS_RESPONSE)
def api_dashboard_hostess():
    return jsonify(dashboard_hostess_service.obtener_dashboard())
