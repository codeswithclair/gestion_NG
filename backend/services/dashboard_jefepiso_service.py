from backend.repositories import dashboard_jefepiso_repository


def obtener_dashboard():
    return dashboard_jefepiso_repository.fetch_dashboard_data()
