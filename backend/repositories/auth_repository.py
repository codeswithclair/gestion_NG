from backend.db import get_cursor


def find_usuario_by_username(nombre_usuario):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                u.no_empleado,
                u.nombre_usuario,
                u.nombre,
                u.apellido,
                u.contrasena,
                u.estado,
                r.nombre AS rol
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.nombre_usuario = %s
        """, (nombre_usuario,))
        return cursor.fetchone()
