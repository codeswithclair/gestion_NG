from flask import Blueprint, jsonify, request

from backend.openapi_spec import doc
from backend.services import auth_service

auth_bp = Blueprint("auth_bp", __name__)

LOGIN_SCHEMA = {
    "type": "object",
    "required": ["nombre_usuario", "contrasena"],
    "properties": {
        "nombre_usuario": {"type": "string"},
        "contrasena": {"type": "string"},
    },
}

LOGIN_RESPONSE = {
    "type": "object",
    "properties": {
        "ok": {"type": "boolean"},
        "usuario": {
            "type": "object",
            "properties": {
                "no_empleado": {"type": "integer"},
                "nombre_usuario": {"type": "string"},
                "nombre_completo": {"type": "string"},
                "rol": {"type": "string"},
            },
        },
    },
}


@auth_bp.route("/api/login", methods=["POST"])
@doc(body=LOGIN_SCHEMA, response=LOGIN_RESPONSE)
def login():
    data = request.get_json()
    usuario = auth_service.login(data.get("nombre_usuario"), data.get("contrasena"))
    return jsonify({"ok": True, "usuario": usuario})
