from backend.db import get_cursor

RESUMEN_FIELDS = """
    COALESCE((
        SELECT g.turno
        FROM Gestion_de_meseros g
        WHERE g.no_empleado = u.no_empleado
          AND g.id_mesa IS NULL
          AND g.fecha_registro = CURDATE()
        ORDER BY g.id_gestion DESC
        LIMIT 1
    ), 'Sin turno') AS turno,

    COALESCE((
        SELECT g.observacion
        FROM Gestion_de_meseros g
        WHERE g.no_empleado = u.no_empleado
          AND g.id_mesa IS NULL
          AND g.fecha_registro = CURDATE()
        ORDER BY g.id_gestion DESC
        LIMIT 1
    ), '') AS observacion,

    COALESCE((
        SELECT g.calificacion
        FROM Gestion_de_meseros g
        WHERE g.no_empleado = u.no_empleado
          AND g.id_mesa IS NULL
          AND g.fecha_registro = CURDATE()
        ORDER BY g.id_gestion DESC
        LIMIT 1
    ), 0) AS calificacion,

    COALESCE((
        SELECT COUNT(*)
        FROM Gestion_de_meseros g
        WHERE g.no_empleado = u.no_empleado
          AND g.id_mesa IS NOT NULL
          AND g.fecha_registro = CURDATE()
    ), 0) AS mesas_atendidas,

    COALESCE((
        SELECT AVG(g.promedio)
        FROM Gestion_de_meseros g
        WHERE g.no_empleado = u.no_empleado
          AND g.id_mesa IS NOT NULL
          AND g.fecha_registro = CURDATE()
    ), 0) AS promedio,

    COALESCE((
        SELECT SUM(pg.cantidad)
        FROM Gestion_de_meseros g
        JOIN Promocion_has_Gestion_de_meseros pg
            ON g.id_gestion = pg.id_gestion
        WHERE g.no_empleado = u.no_empleado
          AND g.fecha_registro = CURDATE()
          AND pg.fecha_aplicacion = CURDATE()
    ), 0) AS promos,

    COALESCE((
        SELECT COUNT(*)
        FROM Mesa m
        WHERE m.no_empleado = u.no_empleado
    ), 0) AS mesas_asignadas
"""


def fetch_resumen_meseros():
    with get_cursor() as (conn, cursor):
        cursor.execute(f"""
            SELECT
                u.no_empleado,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre,
                {RESUMEN_FIELDS}
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE r.id_rol = 'M'
            ORDER BY u.no_empleado
        """)
        return cursor.fetchall()


def fetch_resumen_mesero(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute(f"""
            SELECT
                u.no_empleado,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre,
                {RESUMEN_FIELDS}
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE u.no_empleado = %s
              AND r.id_rol = 'M'
        """, (no_empleado,))
        return cursor.fetchone()


def fetch_resumen_para_ranking():
    """Subconjunto de columnas de todos los meseros, usado solo para calcular ranking."""
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                u.no_empleado,

                COALESCE((
                    SELECT g.calificacion
                    FROM Gestion_de_meseros g
                    WHERE g.no_empleado = u.no_empleado
                      AND g.id_mesa IS NULL
                      AND g.fecha_registro = CURDATE()
                    ORDER BY g.id_gestion DESC
                    LIMIT 1
                ), 0) AS calificacion,

                COALESCE((
                    SELECT SUM(pg.cantidad)
                    FROM Gestion_de_meseros g
                    JOIN Promocion_has_Gestion_de_meseros pg
                        ON g.id_gestion = pg.id_gestion
                    WHERE g.no_empleado = u.no_empleado
                      AND g.fecha_registro = CURDATE()
                      AND pg.fecha_aplicacion = CURDATE()
                ), 0) AS promos,

                COALESCE((
                    SELECT COUNT(*)
                    FROM Gestion_de_meseros g
                    WHERE g.no_empleado = u.no_empleado
                      AND g.id_mesa IS NOT NULL
                      AND g.fecha_registro = CURDATE()
                ), 0) AS mesas_atendidas,

                COALESCE((
                    SELECT AVG(g.promedio)
                    FROM Gestion_de_meseros g
                    WHERE g.no_empleado = u.no_empleado
                      AND g.id_mesa IS NOT NULL
                      AND g.fecha_registro = CURDATE()
                ), 0) AS promedio

            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE r.id_rol = 'M'
        """)
        return cursor.fetchall()


def fetch_mesas_de_mesero(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT id_mesa
            FROM Mesa
            WHERE no_empleado = %s
            ORDER BY id_mesa
        """, (no_empleado,))
        return [row["id_mesa"] for row in cursor.fetchall()]


def fetch_detalle_promos(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                p.nombre,
                SUM(pg.cantidad) AS cantidad
            FROM Gestion_de_meseros g
            JOIN Promocion_has_Gestion_de_meseros pg
                ON g.id_gestion = pg.id_gestion
            JOIN Promocion p
                ON pg.id_promocion = p.id_promocion
            WHERE g.no_empleado = %s
              AND g.fecha_registro = CURDATE()
              AND pg.fecha_aplicacion = CURDATE()
            GROUP BY p.nombre
            ORDER BY cantidad DESC
        """, (no_empleado,))
        return cursor.fetchall()


def ensure_gestion_general(no_empleado):
    """Devuelve el id_gestion "general" (sin mesa) del día, creándolo si no existe."""
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT id_gestion
            FROM Gestion_de_meseros
            WHERE no_empleado = %s
              AND id_mesa IS NULL
              AND fecha_registro = CURDATE()
            ORDER BY id_gestion DESC
            LIMIT 1
        """, (no_empleado,))

        gestion = cursor.fetchone()
        if gestion:
            return gestion["id_gestion"]

        cursor.execute("""
            INSERT INTO Gestion_de_meseros
            (no_empleado, id_mesa, promedio, ranking, turno, observacion, calificacion, fecha_registro)
            VALUES (%s, NULL, 0, 0, NULL, '', 0, CURDATE())
        """, (no_empleado,))
        conn.commit()
        return cursor.lastrowid


def update_calificacion(id_gestion, calificacion):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Gestion_de_meseros
            SET calificacion = %s
            WHERE id_gestion = %s
        """, (calificacion, id_gestion))
        conn.commit()


def update_turno(id_gestion, turno):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Gestion_de_meseros
            SET turno = %s
            WHERE id_gestion = %s
        """, (turno, id_gestion))
        conn.commit()


def get_observacion(id_gestion):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT observacion
            FROM Gestion_de_meseros
            WHERE id_gestion = %s
        """, (id_gestion,))
        row = cursor.fetchone()
        return row["observacion"] if row and row["observacion"] else ""


def set_observacion(id_gestion, observacion):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Gestion_de_meseros
            SET observacion = %s
            WHERE id_gestion = %s
        """, (observacion, id_gestion))
        conn.commit()


def find_promo_gestion(id_promocion, id_gestion):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT cantidad
            FROM Promocion_has_Gestion_de_meseros
            WHERE id_promocion = %s
              AND id_gestion = %s
              AND fecha_aplicacion = CURDATE()
        """, (id_promocion, id_gestion))
        return cursor.fetchone()


def incrementar_promo_gestion(id_promocion, id_gestion, cantidad):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Promocion_has_Gestion_de_meseros
            SET cantidad = cantidad + %s
            WHERE id_promocion = %s
              AND id_gestion = %s
              AND fecha_aplicacion = CURDATE()
        """, (cantidad, id_promocion, id_gestion))
        conn.commit()


def insertar_promo_gestion(id_promocion, id_gestion, cantidad):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Promocion_has_Gestion_de_meseros
            (id_promocion, id_gestion, cantidad, fecha_aplicacion)
            VALUES (%s, %s, %s, CURDATE())
        """, (id_promocion, id_gestion, cantidad))
        conn.commit()


def fetch_promociones_select():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT id_promocion, nombre
            FROM Promocion
            WHERE estado = 1
              AND CURDATE() BETWEEN vigencia_inicio AND vigencia_fin
            ORDER BY nombre
        """)
        return cursor.fetchall()
