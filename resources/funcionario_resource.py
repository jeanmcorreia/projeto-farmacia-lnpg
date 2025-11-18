from flask.views import MethodView
from flask_smorest import Blueprint, abort
from services import funcionario_service

from schemas.funcionario_schema import FuncionarioSchema, FuncionarioResponseSchema

blp = Blueprint('funcionarios', 'funcionarios', url_prefix='/funcionarios', description='Operações de funcionários')

@blp.route('/')
class FuncionariosList(MethodView):

    @blp.response(200, FuncionarioResponseSchema(many=True))
    def get(self):
        '''Retorna lista de funcionários'''
        return funcionario_service.get_todos_funcionarios()
    
    @blp.arguments(FuncionarioSchema)
    @blp.response(201, FuncionarioResponseSchema)
    def post(self, dados_funcionario):
        """Cadastra um funcionario"""
        resultado, status = funcionario_service.criar_funcionario(dados_funcionario)

        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao cadastrar funcionário'))
        
        return resultado
    
@blp.route('/<int:id_funcionario>')
class FuncionarioId(MethodView):

    @blp.response(200, FuncionarioResponseSchema)
    def get(self, id_funcionario):
        '''Retorna um funcionário por ID'''
        funcionario = funcionario_service.get_funcionario_por_id(id_funcionario)
    
        if not funcionario:
            abort(404, message='Funcionário não encontrado')
        
        return funcionario
    
    @blp.arguments(FuncionarioSchema)
    @blp.response(200, FuncionarioResponseSchema)
    def put(self, dados_funcionario, id_funcionario):
        '''Atualiza funcionário por ID'''

        resultado, status = funcionario_service.atualizar_funcionario(id_funcionario, dados_funcionario)

        if status != 200:
            abort(status, message=resultado.get('erro', 'Erro ao atualizar o funcionário'))
        
        return resultado
    
    @blp.response(204)
    def delete(self, id_funcionario):
        '''Deleta funcionário por id'''

        resultado, status = funcionario_service.deletar_funcionario(id_funcionario)

        if status != 204:
            abort(status, message=resultado.get('erro', 'Erro ao deletar o funcionário'))

        return ""

@blp.route('/cargo/<string:cargo>')
class FuncionarioPorCargo(MethodView):

    @blp.response(200, FuncionarioResponseSchema)
    def get(self, cargo):
        '''Retorna lista de funcionários por cargo'''
        funcionarios = funcionario_service.get_funcionarios_por_cargo(cargo)

        if not funcionarios:
            abort(404, message="Funcionários não encontrados")

        return funcionarios