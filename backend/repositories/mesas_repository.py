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


def liberar_y_registrar_atendida(id_mesa, empleado_anterior, minutos_servicio):
    """Inserta el registro de servicio y libera la mesa en una sola transacción."""
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Gestion_de_meseros
            (no_empleado, id_mesa, promedio, ranking, turno, observacion, calificacion)
            VALUES (%s, %s, %s, 0, NULL, '', 0)
        """, (empleado_anterior, id_mesa, minutos_servicio))

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
            SET estado = 'ocupada',
                nombre_cliente = %s,
                no_personas = %s,
                no_empleado = %s,
                hora_inicio = IF(hora_inicio IS NULL, NOW(), hora_inicio),
                razon_retraso = %s,
                comentario_retraso = %s
            WHERE id_mesa = %s
        """, (nombre_cliente, no_personas, no_empleado, razon_retraso, comentario_retraso, id_mesa))
        conn.commit()


def poner_en_limpieza(id_mesa, razon_retraso, comentario_retraso):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Mesa
            SET estado = 'limpieza',
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
