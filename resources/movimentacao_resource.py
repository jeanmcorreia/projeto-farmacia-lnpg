from flask.views import MethodView
from flask_smorest import Blueprint, abort
from services import movimentacao_service

from schemas.movimentacao_schema import MovimentacaoSchema, MovimentacaoResponseSchema 

blp = Blueprint('movimentacoes', 'movimentacoes', url_prefix='/movimentacoes', description='Operações de movimentações')

@blp.route('')
class MovimentacoesList(MethodView):

    @blp.response(200, MovimentacaoResponseSchema(many=True))
    def get(self):
        '''Retorna lista de movimentações'''
        return movimentacao_service.get_todas_movimentacoes()
    
    @blp.arguments(MovimentacaoSchema)
    @blp.response(201, MovimentacaoResponseSchema)
    def post(self, dados_movimentacao):
        '''Registrar uma movimentação'''
        resultado, status = movimentacao_service.add_movimentacao(dados_movimentacao)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao registrar a movimentação'))
        
        return resultado
    
@blp.route('/<int:id_medicamento>')
class MovimentacoesPorMedicamento(MethodView):

    @blp.response(200, MovimentacaoResponseSchema(many=True))
    def get(self, id_medicamento):
        '''Retorna movimentos por medicamento'''
        movimentacao = movimentacao_service.get_movimentacoes_por_medicamento(id_medicamento)

        if not movimentacao:
            abort(404, message="Movimentações não encontradas")
        
        return movimentacao
