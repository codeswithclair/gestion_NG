from backend.repositories import dashboard_mesero_repository


def _nombre_turno(turno):
    if not turno:
        return "Sin turno"

    t = turno.lower()

    if "8" in t:
        return "Matutino"
    if "3" in t or "4" in t:
        return "Vespertino"
    if "6" in t or "1 am" in t:
        return "Nocturno"

    return turno


def obtener_dashboard(no_empleado):
    data = dashboard_mesero_repository.fetch_dashboard_data(no_empleado)

    return {
        "mesas_atendidas": data["mesas_atendidas"],
        "promedio_servicio": round(float(data["promedio_servicio"]), 1),
        "promos": int(data["promos"]),
        "turno": _nombre_turno(data["turno"]),
        "mesas_actuales": data["mesas_actuales"],
    }
