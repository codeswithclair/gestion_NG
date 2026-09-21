from backend.db import get_cursor


def fetch_all():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                id_promocion,
                no_empleado,
                nombre,
                descripcion,
                condiciones,
                vigencia_inicio,
                vigencia_fin,
                estado,
                ocasion,
                dias_vigentes
            FROM Promocion
            ORDER BY id_promocion DESC
        """)
        return cursor.fetchall()


def fetch_vigentes():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                id_promocion,
                nombre,
                descripcion,
                condiciones,
                vigencia_inicio,
                vigencia_fin,
                estado,
                ocasion,
                dias_vigentes
            FROM Promocion
            WHERE estado = 1
              AND CURDATE() BETWEEN vigencia_inicio AND vigencia_fin
            ORDER BY vigencia_fin ASC
        """)
        return cursor.fetchall()


def insert(no_empleado, nombre, descripcion, condiciones, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Promocion
            (no_empleado, nombre, descripcion, condiciones, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (no_empleado, nombre, descripcion, condiciones, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes))
        conn.commit()
        return cursor.lastrowid


def update(id_promocion, nombre, descripcion, condiciones, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Promocion
            SET nombre=%s,
                descripcion=%s,
                condiciones=%s,
                vigencia_inicio=%s,
                vigencia_fin=%s,
                estado=%s,
                ocasion=%s,
                dias_vigentes=%s
            WHERE id_promocion=%s
        """, (nombre, descripcion, condiciones, vigencia_inicio, vigencia_fin, estado, ocasion, dias_vigentes, id_promocion))
        conn.commit()


def update_estado(id_promocion, estado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Promocion
            SET estado = %s
            WHERE id_promocion = %s
        """, (estado, id_promocion))
        conn.commit()


def delete(id_promocion):
    with get_cursor() as (conn, cursor):
        cursor.execute("DELETE FROM Promocion WHERE id_promocion = %s", (id_promocion,))
        conn.commit()


def desactivar(id_promocion):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Promocion
            SET estado = 0
            WHERE id_promocion = %s
        """, (id_promocion,))
        conn.commit()
