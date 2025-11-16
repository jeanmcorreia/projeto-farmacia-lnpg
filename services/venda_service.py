from datetime import datetime

import repositories.venda_db as venda_repo
import repositories.item_venda_db as item_venda_repo
import repositories.db as db_base 

import services.medicamento_service as med_service
import services.movimentacao_service as mov_service

def realizar_venda(dados_venda):
    try:
        itens_processados = []
        valor_total_calculado = 0.0

        for item_req in dados_venda['itens']:
            medicamento = med_service.get_medicamento_por_id(item_req['id_medicamento'])

            if not medicamento:
                return {"erro": f"Medicamento com ID {item_req['id_medicamento']} não encontrado."}, 404
            
            estoque_atual = int(medicamento.get('quantidade_estoque', 0))
            preco_unit = float(medicamento.get('preco_unitario', 0.0))

            if estoque_atual < item_req['quantidade']:
                return {"erro": f"Estoque insuficiente para o medicamento {medicamento['nome']}. Restam {estoque_atual} unidades."}, 400
            
            itens_processados.append({
                "id_medicamento": item_req['id_medicamento'],
                "quantidade": item_req['quantidade'],
                "preco_unitario_momento": preco_unit
            })
            valor_total_calculado += preco_unit * item_req['quantidade']

        
        id_nova_venda = db_base.gerar_id(db_base.VENDAS_CSV)
        nova_venda_dados = {
            'id': id_nova_venda,
            'id_cliente': dados_venda['id_cliente'],
            'id_funcionario': dados_venda['id_funcionario'],
            'data_venda': datetime.now().isoformat(),
            'valor_total': round(valor_total_calculado, 2)
        }
        venda_repo.add_new(nova_venda_dados)

        for item in itens_processados:
            item_data = {
                'id_venda': id_nova_venda,
                'id_medicamento': item['id_medicamento'],
                'quantidade': item['quantidade'],
                'preco_unitario_momento': item['preco_unitario_momento']
            }

            item_data['id'] = db_base.gerar_id(db_base.ITENS_VENDA_CSV)
            item_venda_repo.add_new(item_data)

            mov_service.add_movimentacao({
                'id_medicamento': item['id_medicamento'],
                'tipo': 'saida',
                'quantidade': item['quantidade'],
                'data': datetime.now().isoformat(),
                'id_funcionario': dados_venda['id_funcionario']
            })

        nova_venda_dados['itens'] = itens_processados
        return nova_venda_dados, 201
    
    except Exception as e:
        print(f"Erro ao realizar venda: {e}")
        return {"erro": f"Ocorreu um erro interno no servidor: {e}"}, 500


def get_todas_vendas():
    return venda_repo.get_all()


def get_venda_por_id(id_venda):
    venda = venda_repo.find_by_id(id_venda)
    
    if not venda:
        return None
    
    itens = item_venda_repo.find_by_venda_id(id_venda)
    venda['itens'] = itens
    return venda