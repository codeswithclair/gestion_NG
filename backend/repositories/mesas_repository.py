from backend.db import get_cursor


def fetch_all():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                m.id_mesa,
                m.no_empleado,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre_mesero,
                m.estado,
                m.nombre_cliente,
                m.no_personas,
                m.hora_inicio,
                m.razon_retraso,
                m.comentario_retraso,
                TIMESTAMPDIFF(SECOND, m.hora_inicio, NOW()) AS segundos_transcurridos
            FROM Mesa m
            LEFT JOIN Usuarios u ON m.no_empleado = u.no_empleado
            ORDER BY m.id_mesa
        """)
        return cursor.fetchall()


def get_by_id(id_mesa):
    with get_cursor() as (conn, cursor):
        cursor.execute("SELECT * FROM Mesa WHERE id_mesa = %s", (id_mesa,))
        return cursor.fetchone()


def liberar_y_registrar_atendida(id_mesa, empleado_anterior, minutos_servicio, razon_retraso=None, comentario_retraso=None):
    """Inserta el registro de servicio y libera la mesa en una sola transacción.

    razon_retraso/comentario_retraso se conservan aquí porque la mesa se
    limpia (queda en NULL) al liberarse, y así el motivo de retraso queda
    disponible para los reportes históricos.
    """
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Gestion_de_meseros
            (no_empleado, id_mesa, promedio, ranking, turno, observacion, calificacion, razon_retraso, comentario_retraso)
            VALUES (%s, %s, %s, 0, NULL, '', 0, %s, %s)
        """, (empleado_anterior, id_mesa, minutos_servicio, razon_retraso, comentario_retraso))

        cursor.execute("""
            UPDATE Mesa
            SET estado = 'libre',
                nombre_cliente = NULL,
                no_personas = NULL,
                no_empleado = NULL,
                hora_inicio = NULL,
                razon_retraso = NULL,
                comentario_retraso = NULL
            WHERE id_mesa = %s
        """, (id_mesa,))

        conn.commit()


def ocupar(id_mesa, nombre_cliente, no_personas, no_empleado, razon_retraso, comentario_retraso):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET hora_inicio = IF(estado <> 'ocupada' OR hora_inicio IS NULL, NOW(), hora_inicio),
                estado = 'ocupada',
                nombre_cliente = %s,
                no_personas = %s,
                no_empleado = %s,
                razon_retraso = %s,
                comentario_retraso = %s
            WHERE id_mesa = %s
        """, (nombre_cliente, no_personas, no_empleado, razon_retraso, comentario_retraso, id_mesa))
        conn.commit()


def poner_en_limpieza(id_mesa, razon_retraso, comentario_retraso):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET hora_inicio = IF(estado <> 'limpieza' OR hora_inicio IS NULL, NOW(), hora_inicio),
                estado = 'limpieza',
                nombre_cliente = NULL,
                no_personas = NULL,
                no_empleado = NULL,
                razon_retraso = %s,
                comentario_retraso = %s
            WHERE id_mesa = %s
        """, (razon_retraso, comentario_retraso, id_mesa))
        conn.commit()


def liberar_simple(id_mesa):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET estado = 'libre',
                nombre_cliente = NULL,
                no_personas = NULL,
                no_empleado = NULL,
                hora_inicio = NULL,
                razon_retraso = NULL,
                comentario_retraso = NULL
            WHERE id_mesa = %s
        """, (id_mesa,))
        conn.commit()


def set_estado_generico(id_mesa, estado):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET estado = %s
            WHERE id_mesa = %s
        """, (estado, id_mesa))
        conn.commit()


def guardar_retraso(id_mesa, razon_retraso, comentario_retraso):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET razon_retraso=%s,
                comentario_retraso=%s
            WHERE id_mesa=%s
        """, (razon_retraso, comentario_retraso, id_mesa))
        conn.commit()


def fetch_promedio_atencion(id_mesa=None, fecha_inicio=None, fecha_fin=None):
    """Promedio de minutos de atención (y número de mesas atendidas), filtrable
    por mesa y/o rango de fechas, a partir de los registros históricos en
    Gestion_de_meseros."""
    condiciones = []
    valores = []

    if id_mesa is not None:
        condiciones.append("id_mesa = %s")
        valores.append(id_mesa)
    if fecha_inicio is not None:
        condiciones.append("fecha_registro >= %s")
        valores.append(fecha_inicio)
    if fecha_fin is not None:
        condiciones.append("fecha_registro <= %s")
        valores.append(fecha_fin)

    where_clause = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    with get_cursor() as (conn, cursor):
        cursor.execute(f"""
            SELECT
                AVG(promedio) AS promedio_minutos,
                COUNT(*) AS mesas_atendidas
            FROM Gestion_de_meseros
            {where_clause}
        """, tuple(valores))
        return cursor.fetchone()


def fetch_motivo_retraso_frecuente(fecha_inicio=None, fecha_fin=None):
    """Motivo de retraso más frecuente dentro de un rango de fechas opcional."""
    condiciones = ["razon_retraso IS NOT NULL", "razon_retraso <> ''"]
    valores = []

    if fecha_inicio is not None:
        condiciones.append("fecha_registro >= %s")
        valores.append(fecha_inicio)
    if fecha_fin is not None:
        condiciones.append("fecha_registro <= %s")
        valores.append(fecha_fin)

    where_clause = f"WHERE {' AND '.join(condiciones)}"

    with get_cursor() as (conn, cursor):
        cursor.execute(f"""
            SELECT razon_retraso, COUNT(*) AS total
            FROM Gestion_de_meseros
            {where_clause}
            GROUP BY razon_retraso
            ORDER BY total DESC
            LIMIT 1
        """, tuple(valores))
        return cursor.fetchone()


def fetch_detalle_atenciones(fecha_inicio=None, fecha_fin=None):
    """Detalle de mesas atendidas (para el reporte en PDF)."""
    condiciones = []
    valores = []

    if fecha_inicio is not None:
        condiciones.append("g.fecha_registro >= %s")
        valores.append(fecha_inicio)
    if fecha_fin is not None:
        condiciones.append("g.fecha_registro <= %s")
        valores.append(fecha_fin)

    where_clause = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    with get_cursor() as (conn, cursor):
        cursor.execute(f"""
            SELECT
                g.id_gestion,
                g.id_mesa,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre_mesero,
                g.promedio AS minutos_atencion,
                g.razon_retraso,
                g.fecha_registro
            FROM Gestion_de_meseros g
            LEFT JOIN Usuarios u ON g.no_empleado = u.no_empleado
            {where_clause}
            ORDER BY g.fecha_registro DESC, g.id_gestion DESC
        """, tuple(valores))
        return cursor.fetchall()


def fetch_meseros_disponibles():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                u.no_empleado,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre_completo
            FROM Usuarios u
            JOIN Rol r ON u.id_rol = r.id_rol
            WHERE r.nombre = 'MESERO'
              AND u.estado = 'ACTIVO'
              AND u.no_empleado NOT IN (
                  SELECT no_empleado
                  FROM Mesa
                  WHERE estado = 'ocupada'
                    AND no_empleado IS NOT NULL
              )
        """)
        return cursor.fetchall()
