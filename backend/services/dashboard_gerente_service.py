from backend.repositories import dashboard_gerente_repository


def obtener_dashboard():
    data = dashboard_gerente_repository.fetch_dashboard_data()

    for r in data["reservaciones"]:
        if r["hora"]:
            r["hora"] = str(r["hora"])

    return {
        "usuarios_activos": data["usuarios_activos"],
        "reservaciones_hoy": data["reservaciones_hoy"],
        "promociones_activas": data["promociones_activas"],
        "rendimiento_promedio": round(float(data["rendimiento"]), 1),
        "reservaciones": data["reservaciones"],
        "promociones": data["promociones"],
        "mejores": data["mejores"],
    }
