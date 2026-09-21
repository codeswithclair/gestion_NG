from backend.db import get_cursor


def fetch_all():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                u.no_empleado,
                u.nombre_usuario,
                u.nombre,
                u.apellido,
                u.correo,
                u.estado,
                u.ultimo_acceso,
                r.id_rol,
                r.nombre AS rol
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            ORDER BY u.no_empleado
        """)
        return cursor.fetchall()


def find_rol_by_no_empleado(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT r.nombre AS rol
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.no_empleado = %s
        """, (no_empleado,))
        return cursor.fetchone()


def fetch_roles_by_ids(ids):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT u.no_empleado, r.nombre AS rol
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.no_empleado IN ({})
        """.format(",".join(["%s"] * len(ids))), ids)
        return cursor.fetchall()


def insert(no_empleado, id_rol, nombre, apellido, contrasena, correo, nombre_usuario, estado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Usuarios
            (no_empleado, id_rol, nombre, apellido, contrasena, correo, nombre_usuario, estado, ultimo_acceso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (no_empleado, id_rol, nombre, apellido, contrasena, correo, nombre_usuario, estado))
        conn.commit()


def update(no_empleado, id_rol, nombre, apellido, correo, nombre_usuario, estado, contrasena=None):
    with get_cursor() as (conn, cursor):
        if contrasena:
            cursor.execute("""
                UPDATE Usuarios
                SET id_rol=%s, nombre=%s, apellido=%s, correo=%s,
                    nombre_usuario=%s, estado=%s, contrasena=%s
                WHERE no_empleado=%s
            """, (id_rol, nombre, apellido, correo, nombre_usuario, estado, contrasena, no_empleado))
        else:
            cursor.execute("""
                UPDATE Usuarios
                SET id_rol=%s, nombre=%s, apellido=%s, correo=%s,
                    nombre_usuario=%s, estado=%s
                WHERE no_empleado=%s
            """, (id_rol, nombre, apellido, correo, nombre_usuario, estado, no_empleado))
        conn.commit()


def update_estado(no_empleado, estado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Usuarios
            SET estado = %s
            WHERE no_empleado = %s
        """, (estado, no_empleado))
        conn.commit()


def update_estado_bulk(ids, estado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Usuarios
            SET estado = %s
            WHERE no_empleado IN ({})
        """.format(",".join(["%s"] * len(ids))), [estado] + ids)
        conn.commit()


def delete(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute("DELETE FROM Usuarios WHERE no_empleado = %s", (no_empleado,))
        conn.commit()


def delete_bulk(ids):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            DELETE FROM Usuarios
            WHERE no_empleado IN ({})
        """.format(",".join(["%s"] * len(ids))), ids)
        conn.commit()
