from flask import Blueprint, jsonify, render_template, request
from backend.db import get_connection

mesas_bp = Blueprint("mesas_bp", __name__)

@mesas_bp.route("/estado_mesas")
def vista_estado_mesas():
    return render_template("estado_mesas.html")


@mesas_bp.route("/api/mesas", methods=["GET"])
def obtener_mesas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
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
"""
    cursor.execute(query)
    mesas = cursor.fetchall()

    for m in mesas:
        if m["hora_inicio"]:
            m["hora_inicio"] = m["hora_inicio"].strftime("%Y-%m-%d %H:%M:%S")
        if m["segundos_transcurridos"] is None:
            m["segundos_transcurridos"] = 0

    cursor.close()
    conn.close()

    return jsonify(mesas)


@mesas_bp.route("/api/mesas/<int:id_mesa>", methods=["PUT"])
def actualizar_mesa(id_mesa):
    data = request.get_json()

    nuevo_estado = data.get("estado")
    nombre_cliente = data.get("nombre_cliente")
    no_personas = data.get("no_personas")
    nuevo_no_empleado = data.get("no_empleado")
    razon_retraso = data.get("razon_retraso")
    comentario_retraso = data.get("comentario_retraso")

    if nuevo_no_empleado == "":
        nuevo_no_empleado = None

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Mesa
        WHERE id_mesa = %s
    """, (id_mesa,))

    mesa_anterior = cursor.fetchone()

    if not mesa_anterior:
        cursor.close()
        conn.close()
        return jsonify({"ok": False, "message": "Mesa no encontrada"}), 404

    empleado_anterior = mesa_anterior.get("no_empleado")
    hora_inicio_anterior = mesa_anterior.get("hora_inicio")

    # Cuando una mesa ocupada con mesero pasa a libre,
    # se registra como mesa atendida en Gestion_de_meseros.
    if nuevo_estado == "libre" and empleado_anterior and hora_inicio_anterior:
        cursor.execute("""
            SELECT TIMESTAMPDIFF(MINUTE, %s, NOW()) AS minutos_servicio
        """, (hora_inicio_anterior,))

        tiempo = cursor.fetchone()
        minutos_servicio = tiempo["minutos_servicio"] or 0

        cursor.execute("""
            INSERT INTO Gestion_de_meseros
            (no_empleado, id_mesa, promedio, ranking, turno, observacion, calificacion)
            VALUES (%s, %s, %s, 0, NULL, '', 0)
        """, (
            empleado_anterior,
            id_mesa,
            minutos_servicio
        ))

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
        cursor.close()
        conn.close()

        return jsonify({
            "ok": True,
            "message": "Mesa liberada y registrada como atendida"
        })

    # Si la mesa está ocupada, conserva o inicia el tiempo.
    if nuevo_estado == "ocupada":
        cursor.execute("""
            UPDATE Mesa
            SET estado = %s,
                nombre_cliente = %s,
                no_personas = %s,
                no_empleado = %s,
                hora_inicio = IF(hora_inicio IS NULL, NOW(), hora_inicio),
                razon_retraso = %s,
                comentario_retraso = %s
            WHERE id_mesa = %s
        """, (
            nuevo_estado,
            nombre_cliente,
            no_personas,
            nuevo_no_empleado,
            razon_retraso,
            comentario_retraso,
            id_mesa
        ))

    elif nuevo_estado == "limpieza":
        cursor.execute("""
            UPDATE Mesa
            SET estado = %s,
                razon_retraso = %s,
                comentario_retraso = %s
            WHERE id_mesa = %s
        """, (
            nuevo_estado,
            razon_retraso,
            comentario_retraso,
            id_mesa
        ))

    else:
      if nuevo_estado == "libre":
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
      else:
        cursor.execute("""
            UPDATE Mesa
            SET estado = %s
            WHERE id_mesa = %s
        """, (
            nuevo_estado,
            id_mesa
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "ok": True,
        "message": "Mesa actualizada correctamente"
    })

@mesas_bp.route("/api/mesas/<int:id_mesa>/retraso", methods=["PUT"])
def guardar_retraso(id_mesa):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        UPDATE Mesa
        SET razon_retraso=%s,
            comentario_retraso=%s
        WHERE id_mesa=%s
    """

    values = (
        data.get("razon_retraso"),
        data.get("comentario_retraso", ""),
        id_mesa
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"ok": True, "message": "Razón del retraso guardada"})

@mesas_bp.route("/api/meseros-disponibles", methods=["GET"])
def obtener_meseros_disponibles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
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
    """

    cursor.execute(query)
    meseros = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(meseros)
