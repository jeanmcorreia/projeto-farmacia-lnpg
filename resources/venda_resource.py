from flask_smorest import Blueprint, abort
from services import venda_service

blp = Blueprint('vendas', 'vendas', url_prefix='/vendas', description='Operações de vendas')


@blp.route('/')
class VendasList:
    def get(self):
        """Retorna todas as vendas"""
        return venda_service.get_todas_vendas()

    def post(self, **kwargs):
        """Realiza uma venda"""
        from flask import request
        dados_venda = request.get_json()
        resultado, status = venda_service.realizar_venda(dados_venda)
        
        if status != 201:
            abort(status, message=resultado.get('erro', 'Erro ao realizar venda'))
        
        return resultado, status


@blp.route('/<int:id_venda>')
class VendaItem:
    def get(self, id_venda):
        """Retorna uma venda por ID"""
        venda = venda_service.get_venda_por_id(id_venda)
        if not venda:
            abort(404, message='Venda não encontrada')
        return venda
