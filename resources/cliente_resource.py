from flask.views import MethodView
from flask_smorest import Blueprint, abort
from services import cliente_service

from schemas.cliente_schema import ClienteSchema, ClienteResponseSchema

blp = Blueprint('clientes', 'clientes', url_prefix='/clientes', description='Operações de clientes')

@blp.route('/')
class ClientesList(MethodView):

    @blp.response(200, ClienteResponseSchema(many=True))
    def get(self):
        """Retorna lista de clientes"""
        return cliente_service.get_todos_clientes()
    
    @blp.arguments(ClienteSchema)
    @blp.response(201, ClienteResponseSchema)
    def post(self, dados_cliente):
        """Cadastra um cliente"""
        resultado, status = cliente_service.criar_cliente(dados_cliente)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao cadastrar o cliente'))

        return resultado

@blp.route('/<int:id_cliente>')
class ClienteId(MethodView):

    @blp.response(200, ClienteResponseSchema)
    def get(self, id_cliente):
        """Retorna um cliente por ID"""
        cliente = cliente_service.get_cliente_por_id(id_cliente)

        if not cliente:
            abort(404, message='Cliente não encontrado')

        return cliente
    
    @blp.arguments(ClienteSchema)
    @blp.response(201, ClienteResponseSchema)
    def put(self, dados_cliente, id_cliente):
        """Atualiza cliente por ID"""
    
        resultado, status = cliente_service.atualizar_cliente(id_cliente, dados_cliente)
        
        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao atualizar o cliente'))
        
        return resultado

    @blp.response(204)
    def delete(self, id_cliente):
        """Deleta cliente por ID"""

        resultado, status = cliente_service.deletar_cliente(id_cliente)

        if status != 204:
            abort(status, message=resultado.get('erro', 'Erro ao deletar o cliente'))

        return ""