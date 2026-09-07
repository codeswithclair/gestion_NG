from backend.db import get_cursor


def fetch_en_espera():
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            SELECT
                id_lista,
                no_empleado,
                nombre,
                no_personas,
                tipo_festejo,
                hora_registro,
                estado,
                TIMESTAMPDIFF(SECOND, hora_registro, NOW()) AS segundos_esperando
            FROM Lista_Espera
            WHERE estado = 'EN_ESPERA'
            ORDER BY hora_registro ASC
        """)
        return cursor.fetchall()


def insert(no_empleado, nombre, no_personas, tipo_festejo):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            INSERT INTO Lista_Espera
            (no_empleado, nombre, no_personas, tipo_festejo)
            VALUES (%s, %s, %s, %s)
        """, (no_empleado, nombre, no_personas, tipo_festejo))
        conn.commit()


def update(id_lista, nombre, no_personas, tipo_festejo):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Lista_Espera
            SET nombre = %s,
                no_personas = %s,
                tipo_festejo = %s
            WHERE id_lista = %s
        """, (nombre, no_personas, tipo_festejo, id_lista))
        conn.commit()


def delete(id_lista):
    with get_cursor() as (conn, cursor):
        cursor.execute("DELETE FROM Lista_Espera WHERE id_lista = %s", (id_lista,))
        conn.commit()


def marcar_asignado(id_lista):
    with get_cursor() as (conn, cursor):
        cursor.execute("""
            UPDATE Lista_Espera
            SET estado = 'ASIGNADO'
            WHERE id_lista = %s
        """, (id_lista,))
        conn.commit()
