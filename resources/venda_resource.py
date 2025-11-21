from flask.views import MethodView
from flask_smorest import Blueprint, abort
from services import venda_service
from schemas.venda_schema import VendaSchema, VendaResponseSchema, ItemVendaSchema, ItemVendaResponseSchema

blp = Blueprint('vendas', 'vendas', url_prefix='/vendas', description='Operações de vendas')

@blp.route('')
class VendasList(MethodView):

    @blp.response(200, VendaResponseSchema(many=True))
    def get(self):
        """Retorna todas as vendas"""
        return venda_service.get_todas_vendas()

    @blp.arguments(VendaSchema)
    @blp.response(201, VendaResponseSchema)
    def post(self, dados_venda):
        """Realiza uma venda"""
        resultado, status = venda_service.realizar_venda(dados_venda)
        
        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao realizar venda'))
        
        return resultado


@blp.route('/<int:id_venda>')
class VendaItem(MethodView):

    @blp.response(200, VendaResponseSchema)
    def get(self, id_venda):
        """Retorna uma venda por ID"""
        venda = venda_service.get_venda_por_id(id_venda)
        if not venda:
            abort(404, message='Venda não encontrada')
        return venda
