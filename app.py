from flask import Flask
from flask_smorest import Api
import db_utils

'''
# TIRAR DE COMENTARIO DEPOIS
from resources.clientes import blp as ClientesBlueprint
from resources.funcionarios import blp as FuncionariosBlueprint
from resources.medicamentos import blp as MedicamentosBlueprint
from resources.movimentacoes import blp as MovimentacoesBlueprint
'''
from resources.vendas import blp as VendasBlueprint


app = Flask(__name__)

app.config["API_TITLE"] = "API Farmácia"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

try:
    db_utils.inicializar_db()
    print("Banco de dados (CSV) inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o banco de dados: {e}")

'''
# DESCOMENTAR DEPOIS
api.register_blueprint(ClientesBlueprint)
api.register_blueprint(FuncionariosBlueprint)
api.register_blueprint(MedicamentosBlueprint)
api.register_blueprint(MovimentacoesBlueprint)
'''
api.register_blueprint(VendasBlueprint)
print("Blueprints de vendas registrados com sucesso.")


if __name__ == "__main__":
    print("Servidor iniciando em http://127.0.0.1:5000")
    print("Documentaççao disponível em http://127.0.0.1:5000/docs")
    app.run(debug=True)        
