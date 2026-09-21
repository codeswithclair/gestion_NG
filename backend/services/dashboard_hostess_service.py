from backend.repositories import dashboard_hostess_repository


def obtener_dashboard():
    data = dashboard_hostess_repository.fetch_dashboard_data()

    for r in data["reservaciones"]:
        if r["hora"]:
            r["hora"] = str(r["hora"])

    return {
        "clientes_espera": data["clientes_espera"],
        "mesas_ocupadas": data["mesas_ocupadas"],
        "mesas_libres": data["mesas_libres"],
        "promedio_servicio": round(float(data["promedio_servicio"]), 1),
        "promociones_vigentes": data["promociones_vigentes"],
        "reservaciones": data["reservaciones"],
        "espera": data["espera"],
    }
