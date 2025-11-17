from flask import Flask
from flask_smorest import Api
from repositories import db

# Quando a camada 'resources/' estiver pronta,
# estas linhas devem ser descomentadas.
'''
from resources.cliente_resource import blp as ClientesBlueprint
from resources.funcionario_resource import blp as FuncionariosBlueprint
from resources.medicamento_resource import blp as MedicamentosBlueprint
from resources.movimentacao_resource import blp as MovimentacoesBlueprint
from resources.venda_resource import blp as VendasBlueprint
'''
# --- FIM DOS IMPORTS DO RESOURCE ---


app = Flask(__name__)


app.config["API_TITLE"] = "API Farmácia"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


api = Api(app)


try:
    db.inicializar_db()
    print("Banco de dados (CSV) inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar o banco de dados: {e}")

# (Estas linhas devem ser descomentadas quando a camada 'resources/' estiver pronta)
'''
api.register_blueprint(ClientesBlueprint)
api.register_blueprint(FuncionariosBlueprint)
api.register_blueprint(MedicamentosBlueprint)
api.register_blueprint(MovimentacoesBlueprint)
api.register_blueprint(VendasBlueprint)

print("Todos os blueprints foram registrados com sucesso.")
'''
# --- FIM DO REGISTRO DOS BLUEPRINTS ---

if __name__ == "__main__":
    print("Servidor iniciando em http://127.0.0.1:5000")
    print("Documentação disponível em http://127.0.0.1:5000/docs")
    app.run(debug=True)