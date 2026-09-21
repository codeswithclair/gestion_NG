from backend.db import get_cursor


def fetch_dashboard_data():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Lista_Espera
            WHERE estado = 'ESPERANDO'
        """)
        clientes_espera = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Mesa WHERE estado='ocupada'")
        mesas_ocupadas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM Mesa WHERE estado='libre'")
        mesas_libres = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT AVG(TIMESTAMPDIFF(MINUTE, hora_inicio, NOW())) AS promedio
            FROM Mesa
            WHERE estado='ocupada'
              AND hora_inicio IS NOT NULL
        """)
        promedio_servicio = cursor.fetchone()["promedio"] or 0

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM Promocion
            WHERE estado = 1
              AND CURDATE() BETWEEN vigencia_inicio AND vigencia_fin
        """)
        promociones_vigentes = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT nombre_cliente, no_personas, hora, estado
            FROM Reservacion
            WHERE fecha = CURDATE()
            ORDER BY hora ASC
            LIMIT 4
        """)
        reservaciones = cursor.fetchall()

        cursor.execute("""
            SELECT nombre, no_personas
            FROM Lista_Espera
            WHERE estado = 'ESPERANDO'
            ORDER BY id_lista ASC
            LIMIT 3
        """)
        espera = cursor.fetchall()

        return {
            "clientes_espera": clientes_espera,
            "mesas_ocupadas": mesas_ocupadas,
            "mesas_libres": mesas_libres,
            "promedio_servicio": promedio_servicio,
            "promociones_vigentes": promociones_vigentes,
            "reservaciones": reservaciones,
            "espera": espera,
        }
