from flask import Flask, render_template
from backend.auth import auth_bp
from backend.usuarios import usuarios_bp
from backend.reservaciones import reservaciones_bp
from backend.lista_espera import lista_espera_bp
from backend.mesas import mesas_bp
from backend.promociones import promociones_bp
from backend.meseros import meseros_bp

from backend.dashboard_gerente import dashboard_gerente_bp
from backend.dashboard_hostess import dashboard_hostess_bp
from backend.dashboard_jefepiso import dashboard_jefepiso_bp
from backend.dashboard_mesero import dashboard_mesero_bp


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

@app.route("/")
def home():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
