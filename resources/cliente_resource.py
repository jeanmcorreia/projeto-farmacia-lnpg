from flask_smorest import Blueprint, abort
from services import cliente_service
from flask import request

blp = Blueprint('clientes', 'clientes', url_prefix='/clientes', description='Operações de clientes')

@blp.route('/')
class ClientesList:
    def get(self):
        """Retorna lista de clientes"""
        return cliente_service.get_todos_clientes()
    
    def post(self, **kwargs):
        """Cadastra um cliente"""
        dados_cliente = request.get_json()
        resultado, status = cliente_service.criar_cliente(dados_cliente)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao cadastrar o cliente'))

        return resultado, status

@blp.route('/<int:id_cliente>')
class ClienteId:
    def get(self, id_cliente):
        """Retorna um cliente por ID"""
        cliente = cliente_service.get_cliente_por_id(id_cliente)

        if not cliente:
            abort(404, message='Cliente não encontrado')

        return cliente
    
    def put(self, id_cliente):
        """Atualiza cliente por ID"""
        dados_clientes = request.get_json()
        
        resultado, status = cliente_service.atualizar_cliente(id_cliente, dados_clientes)
        
        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao atualizar o cliente'))
        
        return resultado, status

    def delete(self, id_cliente):
        """Deleta cliente por ID"""

        resultado, status = cliente_service.deletar_cliente(id_cliente)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao deletar o cliente'))

        return resultado, status