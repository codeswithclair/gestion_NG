from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import usuarios_service

usuarios_bp = Blueprint("usuarios_bp", __name__)

USUARIO_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre_usuario": {"type": "string"},
        "nombre": {"type": "string"},
        "apellido": {"type": "string"},
        "correo": {"type": "string"},
        "estado": {"type": "string", "enum": ["ACTIVO", "INACTIVO"]},
        "ultimo_acceso": {"type": "string", "format": "date-time", "nullable": True},
        "id_rol": {"type": "string"},
        "rol": {"type": "string"},
    },
}

USUARIO_SCHEMA = {
    "type": "object",
    "required": ["no_empleado", "id_rol", "nombre", "apellido", "contrasena", "nombre_usuario", "estado"],
    "properties": {
        "no_empleado": {"type": "integer"},
        "id_rol": {"type": "string"},
        "nombre": {"type": "string"},
        "apellido": {"type": "string"},
        "contrasena": {"type": "string"},
        "correo": {"type": "string"},
        "nombre_usuario": {"type": "string"},
        "estado": {"type": "string", "enum": ["ACTIVO", "INACTIVO"]},
    },
}

USUARIO_UPDATE_SCHEMA = {
    "type": "object",
    "required": ["id_rol", "nombre", "apellido", "nombre_usuario", "estado"],
    "properties": {
        "id_rol": {"type": "string"},
        "nombre": {"type": "string"},
        "apellido": {"type": "string"},
        "correo": {"type": "string"},
        "nombre_usuario": {"type": "string"},
        "estado": {"type": "string", "enum": ["ACTIVO", "INACTIVO"]},
        "contrasena": {"type": "string", "description": "Opcional: solo si se quiere cambiar"},
        "rol_sesion": {"type": "string", "description": "Rol de quien hace la petición"},
    },
}

ESTADO_SCHEMA = {
    "type": "object",
    "required": ["estado"],
    "properties": {
        "estado": {"type": "string", "enum": ["ACTIVO", "INACTIVO"]},
        "rol_sesion": {"type": "string"},
    },
}

BULK_ESTADO_SCHEMA = {
    "type": "object",
    "required": ["ids", "estado"],
    "properties": {
        "ids": {"type": "array", "items": {"type": "integer"}},
        "estado": {"type": "string", "enum": ["ACTIVO", "INACTIVO"]},
        "rol_sesion": {"type": "string"},
    },
}

BULK_DELETE_SCHEMA = {
    "type": "object",
    "required": ["ids"],
    "properties": {
        "ids": {"type": "array", "items": {"type": "integer"}},
        "rol_sesion": {"type": "string"},
    },
}


@usuarios_bp.route("/usuarios")
def vista_usuarios():
    return render_template("usuarios.html")


@usuarios_bp.route("/api/usuarios", methods=["GET"])
@doc(response=array_of(USUARIO_ITEM_SCHEMA))
def obtener_usuarios():
    return jsonify(usuarios_service.listar_usuarios())


@usuarios_bp.route("/api/usuarios", methods=["POST"])
@doc(body=USUARIO_SCHEMA, response=OK_RESPONSE)
def crear_usuario():
    resultado = usuarios_service.crear_usuario(request.get_json())
    return jsonify(resultado), 201


@usuarios_bp.route("/api/usuarios/<int:no_empleado>", methods=["PUT"])
@doc(body=USUARIO_UPDATE_SCHEMA, response=OK_RESPONSE)
def actualizar_usuario(no_empleado):
    resultado = usuarios_service.actualizar_usuario(no_empleado, request.get_json())
    return jsonify(resultado)


@usuarios_bp.route("/api/usuarios/<int:no_empleado>/estado", methods=["PUT"])
@doc(body=ESTADO_SCHEMA, response=OK_RESPONSE)
def cambiar_estado_usuario(no_empleado):
    resultado = usuarios_service.cambiar_estado_usuario(no_empleado, request.get_json())
    return jsonify(resultado)


@usuarios_bp.route("/api/usuarios/<int:no_empleado>", methods=["DELETE"])
@doc(body={"type": "object", "properties": {"rol_sesion": {"type": "string"}}}, response=OK_RESPONSE)
def eliminar_usuario(no_empleado):
    data = request.get_json(silent=True) or {}
    resultado = usuarios_service.eliminar_usuario(no_empleado, data.get("rol_sesion"))
    return jsonify(resultado)


@usuarios_bp.route("/api/usuarios/bulk-estado", methods=["PUT"])
@doc(body=BULK_ESTADO_SCHEMA, response=OK_RESPONSE)
def cambiar_estado_masivo():
    resultado = usuarios_service.cambiar_estado_masivo(request.get_json())
    return jsonify(resultado)


@usuarios_bp.route("/api/usuarios/bulk-delete", methods=["DELETE"])
@doc(body=BULK_DELETE_SCHEMA, response=OK_RESPONSE)
def eliminar_masivo():
    resultado = usuarios_service.eliminar_masivo(request.get_json())
    return jsonify(resultado)
