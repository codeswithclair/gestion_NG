from flask import Blueprint, jsonify, render_template, request
from backend.db import get_connection
from datetime import datetime, date, time

reservaciones_bp = Blueprint("reservaciones_bp", __name__)

@reservaciones_bp.route("/reservaciones")
def vista_reservaciones():
    return render_template("reservaciones.html")


def validar_fecha_hora(fecha_str, hora_str):
    try:
        fecha_hora = datetime.strptime(f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, "Formato de fecha u hora inválido"

    ahora = datetime.now()

    if fecha_hora < ahora:
        return False, "No se puede registrar una reservación en una fecha u hora que ya pasó"

    return True, ""


def validar_reservacion(data):
    campos_obligatorios = ["nombre_cliente", "telefono", "fecha", "hora", "no_personas", "estado"]

    for campo in campos_obligatorios:
        if not data.get(campo):
            return False, "Completa todos los campos obligatorios."

    telefono = "".join(digito for digito in str(data["telefono"]) if digito.isdigit())
    if len(telefono) != 10:
        return False, "El telefono debe tener exactamente 10 digitos."

    data["telefono"] = telefono

    valido, mensaje = validar_fecha_hora(data["fecha"], data["hora"])
    if not valido:
        return False, mensaje

    return True, ""


@reservaciones_bp.route("/api/reservaciones", methods=["GET"])
def obtener_reservaciones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
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
    """

    cursor.execute(query)
    reservaciones = cursor.fetchall()

    for r in reservaciones:
        if r["fecha"]:
            r["fecha"] = r["fecha"].strftime("%Y-%m-%d")

        if r["hora"]:
            total_seconds = int(r["hora"].total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            r["hora"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        if r["fecha_registro"]:
            r["fecha_registro"] = r["fecha_registro"].strftime("%Y-%m-%d %H:%M:%S")

    cursor.close()
    conn.close()

    return jsonify(reservaciones)


@reservaciones_bp.route("/api/reservaciones", methods=["POST"])
def crear_reservacion():
    data = request.get_json()

    valido, mensaje = validar_reservacion(data)
    if not valido:
        return jsonify({"ok": False, "message": mensaje}), 400

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO Reservacion
        (no_empleado, nombre_cliente, apellido_cliente, telefono, fecha, hora, no_personas, estado, comentarios)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["no_empleado"],
        data["nombre_cliente"],
        data.get("apellido_cliente", ""),
        data["telefono"],
        data["fecha"],
        data["hora"],
        data["no_personas"],
        data["estado"],
        data.get("comentarios", "")
    )

    cursor.execute(query, values)
    conn.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify({
        "ok": True,
        "message": "Reservación creada correctamente",
        "id_reservacion": nuevo_id
    }), 201


@reservaciones_bp.route("/api/reservaciones/<int:id_reservacion>", methods=["PUT"])
def actualizar_reservacion(id_reservacion):
    data = request.get_json()

    valido, mensaje = validar_reservacion(data)
    if not valido:
        return jsonify({"ok": False, "message": mensaje}), 400

    conn = get_connection()
    cursor = conn.cursor()

    query = """
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
    """

    values = (
        data["nombre_cliente"],
        data.get("apellido_cliente", ""),
        data["telefono"],
        data["fecha"],
        data["hora"],
        data["no_personas"],
        data["estado"],
        data.get("comentarios", ""),
        id_reservacion
    )

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"ok": False, "message": "Reservación no encontrada"}), 404

    cursor.close()
    conn.close()

    return jsonify({"ok": True, "message": "Reservación actualizada correctamente"})


@reservaciones_bp.route("/api/reservaciones/<int:id_reservacion>", methods=["DELETE"])
def eliminar_reservacion(id_reservacion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Reservacion WHERE id_reservacion = %s", (id_reservacion,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"ok": False, "message": "Reservación no encontrada"}), 404

    cursor.close()
    conn.close()

    return jsonify({"ok": True, "message": "Reservación eliminada correctamente"})
