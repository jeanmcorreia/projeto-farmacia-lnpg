from flask_smorest import Blueprint, abort
from services import medicamento_service
from flask import request

blp = Blueprint('medicamentos', 'medicamentos', url_prefix='/medicamentos', description='Operações com medicamentos')

@blp.route('/')
class MedicamentosList:
    def get(self):
        '''Retorna lista de medicamentos'''
        return medicamento_service.get_todos_medicamentos()
    
    def post(self, **kwargs):
        '''Cadastra um medicamento'''
        dados_medicamento = request.get_json()
        resultado, status = medicamento_service.criar_medicamento(dados_medicamento)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao cadastrar o medicamento'))
        
        return resultado, status
    
@blp.route('/<int:id_medicamento')
class MedicamentoId:
    def get(self, id_medicamento):
        '''Retorna um medicamento por id'''
        medicamento = medicamento_service.get_medicamento_por_id(id_medicamento)

        if not medicamento:
            abort(404, message='Medicamento não encontrado')

        return medicamento
    
    def put(self, id_medicamento):
        '''Atualiza medicamento por id'''
        dados_medicamento = request.get_json()

        resultado, status = medicamento_service.atualizar_medicamento(id_medicamento, dados_medicamento)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao atualizar o medicamento'))

        return resultado, status
    
    def delete(self, id_medicamento):
        '''Deleta medicamento por id'''
        
        resultado, status = medicamento_service.deletar_medicamento(id_medicamento)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao deletar o medicamento'))
        
        return resultado, status