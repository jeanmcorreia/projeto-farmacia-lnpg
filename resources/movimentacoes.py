from flask_smorest import Blueprint, abort
from services import movimentacao_service
from flask import request

blp = Blueprint('movimentacoes', 'movimentacoes', url_prefix='/movimentacoes', description='Operações de movimentações')

@blp.route('/')
class MovimentacoesList:
    def get(self):
        '''Retorna lista de movimentações'''
        return movimentacao_service.get_todas_movimentacoes()
    
    def post(self, **kwargs):
        '''Registrar uma movimentação'''
        dados_movimentacao = request.get_json()
        resultado, status = movimentacao_service.add_movimentacao(dados_movimentacao)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao registrar a movimentação'))
        
        return resultado, status
    
@blp.route('/<int:id_medicamento')
class MovimentacaoPorMedicamento:
    def get(self, id_medicamento):
        '''Retorna movimentos por medicamento'''