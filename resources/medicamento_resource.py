from flask.views import MethodView
from flask_smorest import Blueprint, abort
from services import medicamento_service

from schemas.medicamento_schema import MedicamentoSchema, MedicamentoResponseSchema

blp = Blueprint('medicamentos', 'medicamentos', url_prefix='/medicamentos', description='Operações com medicamentos')

@blp.route('')
class MedicamentosList(MethodView):

    @blp.response(200, MedicamentoResponseSchema(many=True))
    def get(self):
        '''Retorna lista de medicamentos'''
        return medicamento_service.get_todos_medicamentos()
    
    @blp.arguments(MedicamentoSchema)
    @blp.response(201, MedicamentoResponseSchema)
    def post(self, dados_medicamento):
        '''Cadastra um medicamento'''

        resultado, status = medicamento_service.criar_medicamento(dados_medicamento)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao cadastrar o medicamento'))
        
        return resultado
    
@blp.route('/<int:id_medicamento>')
class MedicamentoId(MethodView):

    @blp.response(200, MedicamentoResponseSchema)
    def get(self, id_medicamento):
        '''Retorna um medicamento por id'''
        medicamento = medicamento_service.get_medicamento_por_id(id_medicamento)

        if not medicamento:
            abort(404, message='Medicamento não encontrado')

        return medicamento
    
    @blp.arguments(MedicamentoSchema)
    @blp.response(200, MedicamentoResponseSchema)
    def put(self, dados_medicamento, id_medicamento):
        '''Atualiza medicamento por id'''

        resultado, status = medicamento_service.atualizar_medicamento(id_medicamento, dados_medicamento)

        if status != 200:
            abort(status, message=resultado.get('erro', 'Erro ao atualizar o medicamento'))

        return resultado, status
    
    @blp.response(204)
    def delete(self, id_medicamento):
        '''Deleta medicamento por id'''
        
        resultado, status = medicamento_service.deletar_medicamento(id_medicamento)

        if status != 204:
            abort(status, message=resultado.get('erro', 'Erro ao deletar o medicamento'))
        
        return ""