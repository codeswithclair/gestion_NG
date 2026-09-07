from flask import Blueprint, jsonify, render_template, request

from backend.openapi_spec import OK_RESPONSE, array_of, doc
from backend.services import lista_espera_service

lista_espera_bp = Blueprint("lista_espera_bp", __name__)

CLIENTE_SCHEMA = {
    "type": "object",
    "required": ["no_empleado", "nombre", "no_personas"],
    "properties": {
        "no_empleado": {"type": "integer"},
        "nombre": {"type": "string"},
        "no_personas": {"type": "integer"},
        "tipo_festejo": {"type": "string"},
    },
}

CLIENTE_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "id_lista": {"type": "integer"},
        "no_empleado": {"type": "integer"},
        "nombre": {"type": "string"},
        "no_personas": {"type": "integer"},
        "tipo_festejo": {"type": "string"},
        "hora_registro": {"type": "string", "format": "date-time"},
        "estado": {"type": "string"},
        "segundos_esperando": {"type": "integer"},
    },
}


@lista_espera_bp.route("/lista_espera")
def vista_lista_espera():
    return render_template("lista_espera.html")


@lista_espera_bp.route("/api/lista-espera", methods=["GET"])
@doc(response=array_of(CLIENTE_ITEM_SCHEMA))
def obtener_lista_espera():
    return jsonify(lista_espera_service.listar_en_espera())


@lista_espera_bp.route("/api/lista-espera", methods=["POST"])
@doc(body=CLIENTE_SCHEMA, response=OK_RESPONSE)
def agregar_cliente():
    resultado = lista_espera_service.agregar_cliente(request.get_json())
    return jsonify(resultado), 201


@lista_espera_bp.route("/api/lista-espera/<int:id_lista>", methods=["PUT"])
@doc(body=CLIENTE_SCHEMA, response=OK_RESPONSE)
def actualizar_cliente(id_lista):
    resultado = lista_espera_service.actualizar_cliente(id_lista, request.get_json())
    return jsonify(resultado)


@lista_espera_bp.route("/api/lista-espera/<int:id_lista>", methods=["DELETE"])
@doc(response=OK_RESPONSE)
def eliminar_cliente(id_lista):
    resultado = lista_espera_service.eliminar_cliente(id_lista)
    return jsonify(resultado)


@lista_espera_bp.route("/api/lista-espera/<int:id_lista>/asignar", methods=["PUT"])
@doc(response=OK_RESPONSE)
def asignar_cliente(id_lista):
    resultado = lista_espera_service.asignar_cliente(id_lista)
    return jsonify(resultado)
