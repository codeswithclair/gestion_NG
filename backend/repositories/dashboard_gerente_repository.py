from backend.db import get_cursor


def fetch_dashboard_data():
    with get_cursor() as (conn, cursor):
        cursor.execute("SELECT COUNT(*) AS total FROM Usuarios WHERE estado='ACTIVO'")
        usuarios_activos = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Reservacion WHERE fecha = CURDATE()")
        reservaciones_hoy = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Promocion
            WHERE estado = 1
              AND CURDATE() BETWEEN vigencia_inicio AND vigencia_fin
        """)
        promociones_activas = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT AVG(calificacion) AS promedio
            FROM Gestion_de_meseros
            WHERE id_mesa IS NULL
              AND fecha_registro = CURDATE()
        """)
        rendimiento = cursor.fetchone()["promedio"] or 0

        cursor.execute("""
            SELECT nombre_cliente, no_personas, hora, estado
            FROM Reservacion
            WHERE fecha = CURDATE()
            ORDER BY hora ASC
            LIMIT 2
        """)
        reservaciones = cursor.fetchall()

        cursor.execute("""
            SELECT nombre
            FROM Promocion
            WHERE estado = 1
              AND CURDATE() BETWEEN vigencia_inicio AND vigencia_fin
            ORDER BY id_promocion DESC
            LIMIT 2
        """)
        promociones = cursor.fetchall()

        cursor.execute("""
            SELECT CONCAT(u.nombre, ' ', u.apellido) AS nombre, g.calificacion
            FROM Gestion_de_meseros g
            JOIN Usuarios u ON g.no_empleado = u.no_empleado
            WHERE g.id_mesa IS NULL
              AND g.fecha_registro = CURDATE()
            ORDER BY g.calificacion DESC
            LIMIT 2
        """)
        mejores = cursor.fetchall()

        return {
            "usuarios_activos": usuarios_activos,
            "reservaciones_hoy": reservaciones_hoy,
            "promociones_activas": promociones_activas,
            "rendimiento": rendimiento,
            "reservaciones": reservaciones,
            "promociones": promociones,
            "mejores": mejores,
        }
