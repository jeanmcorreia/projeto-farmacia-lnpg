from flask import Flask, render_template
from flask_smorest import Api
from repositories import db

from resources.cliente_resource import blp as ClientesBlueprint
from resources.funcionario_resource import blp as FuncionariosBlueprint
from resources.medicamento_resource import blp as MedicamentosBlueprint
from resources.movimentacao_resource import blp as MovimentacoesBlueprint
from resources.venda_resource import blp as VendasBlueprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Configurações do API Docs
app.config["API_TITLE"] = "API Farmácia"
app.config["API_VERSION"] = "1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
# Ajustes para compatibilidade DO POSTMAN VS CODE
app.config["OPENAPI_GENERATE_OPERATION_ID"] = True
app.config["OPENAPI_STRIP_URL_PREFIX"] = True
app.config["OPENAPI_PARAMETER_PLACEMENT"] = "method"
app.config["OPENAPI_PREFER_200_FOR_PUT"] = True

api = Api(app)


try:
    db.inicializar_db()
    print("Banco de dados (CSV) inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o banco de dados: {e}")

api.register_blueprint(ClientesBlueprint)
api.register_blueprint(FuncionariosBlueprint)
api.register_blueprint(MedicamentosBlueprint)
api.register_blueprint(MovimentacoesBlueprint)
api.register_blueprint(VendasBlueprint)

print("Todos os blueprints foram registrados com sucesso.")

# --- FIM DO REGISTRO DOS BLUEPRINTS ---

if __name__ == "__main__":
    print("Servidor iniciando em http://127.0.0.1:5000")
    print("Documentação disponível em http://127.0.0.1:5000/docs")
    app.run(debug=True)