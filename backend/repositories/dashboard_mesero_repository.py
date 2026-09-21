from backend.db import get_cursor


def fetch_dashboard_data(no_empleado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Gestion_de_meseros
            WHERE no_empleado = %s
              AND id_mesa IS NOT NULL
              AND fecha_registro = CURDATE()
        """, (no_empleado,))
        mesas_atendidas = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT AVG(promedio) AS promedio
            FROM Gestion_de_meseros
            WHERE no_empleado = %s
              AND id_mesa IS NOT NULL
              AND fecha_registro = CURDATE()
        """, (no_empleado,))
        promedio_servicio = cursor.fetchone()["promedio"] or 0

        cursor.execute("""
            SELECT COALESCE(SUM(pg.cantidad), 0) AS total
            FROM Gestion_de_meseros g
            JOIN Promocion_has_Gestion_de_meseros pg
                ON g.id_gestion = pg.id_gestion
            WHERE g.no_empleado = %s
              AND g.fecha_registro = CURDATE()
              AND pg.fecha_aplicacion = CURDATE()
        """, (no_empleado,))
        promos = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT turno
            FROM Gestion_de_meseros
            WHERE no_empleado = %s
              AND id_mesa IS NULL
              AND fecha_registro = CURDATE()
            ORDER BY id_gestion DESC
            LIMIT 1
        """, (no_empleado,))
        turno_row = cursor.fetchone()
        turno = turno_row["turno"] if turno_row else None

        cursor.execute("""
            SELECT id_mesa, estado, TIMESTAMPDIFF(MINUTE, hora_inicio, NOW()) AS minutos
            FROM Mesa
            WHERE no_empleado = %s
            ORDER BY id_mesa
        """, (no_empleado,))
        mesas_actuales = cursor.fetchall()

        return {
            "mesas_atendidas": mesas_atendidas,
            "promedio_servicio": promedio_servicio,
            "promos": promos,
            "turno": turno,
            "mesas_actuales": mesas_actuales,
        }
