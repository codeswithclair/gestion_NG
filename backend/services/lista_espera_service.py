from backend.repositories import lista_espera_repository


def _formatear(item):
    if item["hora_registro"]:
        item["hora_registro"] = item["hora_registro"].strftime("%Y-%m-%d %H:%M:%S")
    return item


def listar_en_espera():
    return [_formatear(item) for item in lista_espera_repository.fetch_en_espera()]


def agregar_cliente(data):
    lista_espera_repository.insert(
        data["no_empleado"],
        data["nombre"],
        data["no_personas"],
        data.get("tipo_festejo", ""),
    )
    return {"ok": True, "message": "Cliente agregado a la lista"}


def actualizar_cliente(id_lista, data):
    lista_espera_repository.update(
        id_lista,
        data["nombre"],
        data["no_personas"],
        data.get("tipo_festejo", ""),
    )
    return {"ok": True, "message": "Cliente actualizado correctamente"}


def eliminar_cliente(id_lista):
    lista_espera_repository.delete(id_lista)
    return {"ok": True, "message": "Cliente eliminado de la lista"}


def asignar_cliente(id_lista):
    lista_espera_repository.marcar_asignado(id_lista)
    return {"ok": True, "message": "Cliente listo para asignar mesa"}
