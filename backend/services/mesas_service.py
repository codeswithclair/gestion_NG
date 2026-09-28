from datetime import datetime

from backend.errors import ServiceError
from backend.repositories import mesas_repository


def _formatear(mesa):
    if mesa["hora_inicio"]:
        mesa["hora_inicio"] = mesa["hora_inicio"].strftime("%Y-%m-%d %H:%M:%S")
    if mesa["segundos_transcurridos"] is None:
        mesa["segundos_transcurridos"] = 0
    return mesa


def listar_mesas():
    return [_formatear(m) for m in mesas_repository.fetch_all()]


def actualizar_mesa(id_mesa, data):
    nuevo_estado = data.get("estado")
    nombre_cliente = data.get("nombre_cliente")
    no_personas = data.get("no_personas")
    nuevo_no_empleado = data.get("no_empleado")
    razon_retraso = data.get("razon_retraso")
    comentario_retraso = data.get("comentario_retraso")

    if nuevo_no_empleado == "":
        nuevo_no_empleado = None

    mesa_anterior = mesas_repository.get_by_id(id_mesa)
    if not mesa_anterior:
        raise ServiceError("Mesa no encontrada", 404)

    empleado_anterior = mesa_anterior.get("no_empleado")
    hora_inicio_anterior = mesa_anterior.get("hora_inicio")

    # Cuando una mesa ocupada con mesero pasa a libre,
    # se registra como mesa atendida en Gestion_de_meseros.
    if nuevo_estado == "libre" and empleado_anterior and hora_inicio_anterior:
        minutos_servicio = int((datetime.now() - hora_inicio_anterior).total_seconds() // 60)
        mesas_repository.liberar_y_registrar_atendida(
            id_mesa,
            empleado_anterior,
            minutos_servicio,
            mesa_anterior.get("razon_retraso"),
            mesa_anterior.get("comentario_retraso"),
        )
        return {"ok": True, "message": "Mesa liberada y registrada como atendida"}

    if nuevo_estado == "ocupada":
        mesas_repository.ocupar(id_mesa, nombre_cliente, no_personas, nuevo_no_empleado, razon_retraso, comentario_retraso)
    elif nuevo_estado == "limpieza":
        mesas_repository.poner_en_limpieza(id_mesa, razon_retraso, comentario_retraso)
    elif nuevo_estado == "libre":
        mesas_repository.liberar_simple(id_mesa)
    else:
        mesas_repository.set_estado_generico(id_mesa, nuevo_estado)

    return {"ok": True, "message": "Mesa actualizada correctamente"}


def guardar_retraso(id_mesa, data):
    mesas_repository.guardar_retraso(
        id_mesa,
        data.get("razon_retraso"),
        data.get("comentario_retraso", ""),
    )
    return {"ok": True, "message": "Razón del retraso guardada"}


def listar_meseros_disponibles():
    return mesas_repository.fetch_meseros_disponibles()


def _parse_fecha(valor, nombre_campo):
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        raise ServiceError(f"{nombre_campo} debe tener formato YYYY-MM-DD", 400)


def _resolver_rango_fechas(params):
    """Acepta ?fecha=YYYY-MM-DD (un solo día) o ?fecha_inicio=&fecha_fin= (rango)."""
    fecha = params.get("fecha")
    if fecha:
        dia = _parse_fecha(fecha, "fecha")
        return dia, dia

    fecha_inicio = _parse_fecha(params.get("fecha_inicio"), "fecha_inicio")
    fecha_fin = _parse_fecha(params.get("fecha_fin"), "fecha_fin")

    if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
        raise ServiceError("fecha_inicio no puede ser posterior a fecha_fin", 400)

    return fecha_inicio, fecha_fin


def obtener_promedio_atencion(params):
    id_mesa = params.get("id_mesa")
    if id_mesa not in (None, ""):
        try:
            id_mesa = int(id_mesa)
        except (TypeError, ValueError):
            raise ServiceError("id_mesa debe ser un número entero", 400)
    else:
        id_mesa = None

    fecha_inicio, fecha_fin = _resolver_rango_fechas(params)
    resultado = mesas_repository.fetch_promedio_atencion(id_mesa, fecha_inicio, fecha_fin) or {}

    promedio = resultado.get("promedio_minutos")
    return {
        "promedio_minutos": round(float(promedio), 1) if promedio is not None else 0,
        "mesas_atendidas": resultado.get("mesas_atendidas") or 0,
    }


def obtener_motivo_retraso_frecuente(params):
    fecha_inicio, fecha_fin = _resolver_rango_fechas(params)
    resultado = mesas_repository.fetch_motivo_retraso_frecuente(fecha_inicio, fecha_fin)

    if not resultado:
        return {"motivo": None, "total": 0}

    return {"motivo": resultado["razon_retraso"], "total": resultado["total"]}


def obtener_resumen_reporte(params):
    fecha_inicio, fecha_fin = _resolver_rango_fechas(params)
    promedio_resultado = mesas_repository.fetch_promedio_atencion(None, fecha_inicio, fecha_fin) or {}
    motivo_resultado = mesas_repository.fetch_motivo_retraso_frecuente(fecha_inicio, fecha_fin)

    promedio = promedio_resultado.get("promedio_minutos")

    return {
        "fecha_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
        "fecha_fin": fecha_fin.isoformat() if fecha_fin else None,
        "promedio_minutos": round(float(promedio), 1) if promedio is not None else 0,
        "mesas_atendidas": promedio_resultado.get("mesas_atendidas") or 0,
        "motivo_mas_frecuente": motivo_resultado["razon_retraso"] if motivo_resultado else None,
        "motivo_total": motivo_resultado["total"] if motivo_resultado else 0,
    }


def generar_reporte_pdf(params):
    """Construye el reporte de mesas y retrasos en PDF (resumen + detalle)."""
    from io import BytesIO

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    resumen = obtener_resumen_reporte(params)
    fecha_inicio, fecha_fin = _resolver_rango_fechas(params)
    detalle = mesas_repository.fetch_detalle_atenciones(fecha_inicio, fecha_fin)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="Reporte de mesas y retrasos")
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Reporte de mesas y retrasos", styles["Title"]))
    rango = f"{resumen['fecha_inicio'] or 'inicio de registros'} — {resumen['fecha_fin'] or 'hoy'}"
    elementos.append(Paragraph(f"Rango de fechas: {rango}", styles["Normal"]))
    elementos.append(Spacer(1, 12))

    resumen_data = [
        ["Promedio de atención (min)", str(resumen["promedio_minutos"])],
        ["Mesas atendidas", str(resumen["mesas_atendidas"])],
        ["Motivo de retraso más común", resumen["motivo_mas_frecuente"] or "Sin registros"],
    ]
    tabla_resumen = Table(resumen_data, colWidths=[9 * cm, 6 * cm])
    tabla_resumen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla_resumen)
    elementos.append(Spacer(1, 18))

    elementos.append(Paragraph("Detalle de mesas atendidas", styles["Heading2"]))
    encabezados = ["Mesa", "Mesero", "Minutos", "Motivo de retraso", "Fecha"]
    filas = [encabezados]
    for fila in detalle:
        filas.append([
            str(fila["id_mesa"]),
            fila["nombre_mesero"] or "—",
            str(fila["minutos_atencion"]) if fila["minutos_atencion"] is not None else "—",
            fila["razon_retraso"] or "—",
            fila["fecha_registro"].strftime("%Y-%m-%d") if fila["fecha_registro"] else "—",
        ])

    if len(filas) == 1:
        filas.append(["—", "—", "—", "Sin registros en el rango seleccionado", "—"])

    tabla_detalle = Table(filas, colWidths=[2 * cm, 4 * cm, 2.2 * cm, 5.3 * cm, 2.5 * cm], repeatRows=1)
    tabla_detalle.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f3b52")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
    ]))
    elementos.append(tabla_detalle)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
