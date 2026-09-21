from backend.errors import ServiceError
from backend.repositories import usuarios_repository


def _formatear(usuario):
    if usuario.get("ultimo_acceso"):
        usuario["ultimo_acceso"] = usuario["ultimo_acceso"].strftime("%Y-%m-%d %H:%M:%S")
    return usuario


def listar_usuarios():
    return [_formatear(u) for u in usuarios_repository.fetch_all()]


def crear_usuario(data):
    usuarios_repository.insert(
        data["no_empleado"],
        data["id_rol"],
        data["nombre"],
        data["apellido"],
        data["contrasena"],
        data.get("correo", ""),
        data["nombre_usuario"],
        data["estado"],
    )
    return {"ok": True, "message": "Usuario registrado correctamente"}


def actualizar_usuario(no_empleado, data):
    usuario_actual = usuarios_repository.find_rol_by_no_empleado(no_empleado)
    if not usuario_actual:
        raise ServiceError("Usuario no encontrado", 404)

    rol_sesion = data.get("rol_sesion")

    if rol_sesion == "JEFEPISO" and usuario_actual["rol"] == "GERENTE":
        raise ServiceError("El jefe de piso no puede modificar cuentas de gerente", 403)

    if rol_sesion == "JEFEPISO" and usuario_actual["rol"] not in ["HOSTESS", "MESERO"]:
        raise ServiceError("Solo puede modificar personal operativo", 403)

    usuarios_repository.update(
        no_empleado,
        data["id_rol"],
        data["nombre"],
        data["apellido"],
        data.get("correo", ""),
        data["nombre_usuario"],
        data["estado"],
        contrasena=data.get("contrasena"),
    )
    return {"ok": True, "message": "Usuario actualizado correctamente"}


def cambiar_estado_usuario(no_empleado, data):
    nuevo_estado = data["estado"]
    rol_sesion = data.get("rol_sesion")

    usuario = usuarios_repository.find_rol_by_no_empleado(no_empleado)
    if not usuario:
        raise ServiceError("Usuario no encontrado", 404)

    if rol_sesion == "JEFEPISO" and usuario["rol"] == "GERENTE":
        raise ServiceError("No puedes modificar a un gerente", 403)

    usuarios_repository.update_estado(no_empleado, nuevo_estado)
    return {"ok": True, "message": "Estado actualizado correctamente"}


def eliminar_usuario(no_empleado, rol_sesion):
    if rol_sesion != "GERENTE":
        raise ServiceError("Solo gerente puede eliminar usuarios", 403)

    usuarios_repository.delete(no_empleado)
    return {"ok": True, "message": "Usuario eliminado correctamente"}


def cambiar_estado_masivo(data):
    ids = data["ids"]
    estado = data["estado"]
    rol_sesion = data.get("rol_sesion")

    if rol_sesion == "JEFEPISO":
        encontrados = usuarios_repository.fetch_roles_by_ids(ids)
        if any(u["rol"] == "GERENTE" for u in encontrados):
            raise ServiceError("No puedes modificar gerentes", 403)

    usuarios_repository.update_estado_bulk(ids, estado)
    return {"ok": True, "message": "Usuarios actualizados correctamente"}


def eliminar_masivo(data):
    ids = data["ids"]
    rol_sesion = data.get("rol_sesion")

    if rol_sesion != "GERENTE":
        raise ServiceError("Solo gerente puede eliminar usuarios", 403)

    usuarios_repository.delete_bulk(ids)
    return {"ok": True, "message": "Usuarios eliminados correctamente"}
