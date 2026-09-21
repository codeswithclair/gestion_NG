from flask import Blueprint, jsonify, render_template

from backend.openapi_spec import doc
from backend.services import dashboard_mesero_service

dashboard_mesero_bp = Blueprint("dashboard_mesero_bp", __name__)

DASHBOARD_MESERO_RESPONSE = {
    "type": "object",
    "properties": {
        "mesas_atendidas": {"type": "integer"},
        "promedio_servicio": {"type": "number"},
        "promos": {"type": "integer"},
        "turno": {"type": "string"},
        "mesas_actuales": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id_mesa": {"type": "integer"},
                    "estado": {"type": "string"},
                    "minutos": {"type": "integer", "nullable": True},
                },
            },
        },
    },
}


@dashboard_mesero_bp.route("/mesero")
def mesero_dashboard():
    return render_template("mesero_dashboard.html")


@dashboard_mesero_bp.route("/api/dashboard/mesero/<int:no_empleado>")
@doc(response=DASHBOARD_MESERO_RESPONSE)
def api_dashboard_mesero(no_empleado):
    return jsonify(dashboard_mesero_service.obtener_dashboard(no_empleado))
