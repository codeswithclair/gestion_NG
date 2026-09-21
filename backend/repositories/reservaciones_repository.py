from backend.db import get_cursor


def fetch_all():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                r.id_reservacion,
                r.no_empleado,
                r.nombre_cliente,
                r.apellido_cliente,
                r.telefono,
                r.fecha,
                r.hora,
                r.fecha_registro,
                r.no_personas,
                r.estado,
                r.comentarios
            FROM Reservacion r
            ORDER BY
                CASE
                    WHEN TIMESTAMP(r.fecha, r.hora) >= NOW() THEN 0
                    ELSE 1
                END,
                r.fecha ASC,
                r.hora ASC
        """)
        return cursor.fetchall()


def insert(no_empleado, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Reservacion
            (no_empleado, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (no_empleado, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios))
        conn.commit()
        return cursor.lastrowid


def update(id_reservacion, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Reservacion
            SET nombre_cliente=%s,
                apellido_cliente=%s,
                telefono=%s,
                fecha=%s,
                hora=%s,
                no_personas=%s,
                estado=%s,
                comentarios=%s
            WHERE id_reservacion=%s
        """, (nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios, id_reservacion))
        conn.commit()
        return cursor.rowcount


def delete(id_reservacion):
    with get_cursor() as (conn, cursor):
        cursor.execute("DELETE FROM Reservacion WHERE id_reservacion = %s", (id_reservacion,))
        conn.commit()
        return cursor.rowcount
