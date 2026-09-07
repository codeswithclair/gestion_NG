from flask import Flask, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint

from backend.errors import ServiceError
from backend.openapi_spec import build_spec

from backend.controllers.auth_controller import auth_bp
from backend.controllers.usuarios_controller import usuarios_bp
from backend.controllers.reservaciones_controller import reservaciones_bp
from backend.controllers.lista_espera_controller import lista_espera_bp
from backend.controllers.mesas_controller import mesas_bp
from backend.controllers.promociones_controller import promociones_bp
from backend.controllers.meseros_controller import meseros_bp

from backend.controllers.dashboard_gerente_controller import dashboard_gerente_bp
from backend.controllers.dashboard_hostess_controller import dashboard_hostess_bp
from backend.controllers.dashboard_jefepiso_controller import dashboard_jefepiso_bp
from backend.controllers.dashboard_mesero_controller import dashboard_mesero_bp


app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(reservaciones_bp)
app.register_blueprint(lista_espera_bp)
app.register_blueprint(mesas_bp)
app.register_blueprint(promociones_bp)
app.register_blueprint(meseros_bp)
app.register_blueprint(dashboard_gerente_bp)
app.register_blueprint(dashboard_hostess_bp)
app.register_blueprint(dashboard_jefepiso_bp)
app.register_blueprint(dashboard_mesero_bp)


@app.errorhandler(ServiceError)
def handle_service_error(err):
    return jsonify({"ok": False, "message": err.message}), err.status_code


SWAGGER_URL = "/docs"
API_URL = "/openapi.json"

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Gestion NG API"},
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)


@app.route(API_URL)
def openapi_spec():
    return jsonify(build_spec(app))


@app.route("/")
def home():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
