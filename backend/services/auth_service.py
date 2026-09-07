from backend.errors import ServiceError
from backend.repositories import auth_repository


def login(nombre_usuario, contrasena):
    if not nombre_usuario or not contrasena:
        raise ServiceError("Faltan credenciales", 400)

    usuario = auth_repository.find_usuario_by_username(nombre_usuario)

    if not usuario:
        raise ServiceError("El usuario no existe", 404)

    if usuario["contrasena"] != contrasena:
        raise ServiceError("Contraseña incorrecta", 401)

    if usuario["estado"] != "ACTIVO":
        raise ServiceError("El usuario no está activo", 403)

    return {
        "no_empleado": usuario["no_empleado"],
        "nombre_usuario": usuario["nombre_usuario"],
        "nombre_completo": f"{usuario['nombre']} {usuario['apellido']}",
        "rol": usuario["rol"],
    }
