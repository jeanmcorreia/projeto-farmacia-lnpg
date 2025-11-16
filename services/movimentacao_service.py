import repositories.movimentacao_db as mov_repo
import repositories.medicamento_db as med_repo
import repositories.db as db_base
from datetime import datetime

def add_movimentacao(dados_movimentacao):
    medicamento = med_repo.find_by_id(dados_movimentacao['id_medicamento'])
    if not medicamento:
        raise Exception("Medicamento não encontrado na movimentação")

    estoque_atual = int(medicamento.get('quantidade_estoque', 0))
    quantidade_mov = int(dados_movimentacao['quantidade'])

    if dados_movimentacao['tipo'] == 'saida':
        novo_estoque = estoque_atual - quantidade_mov
    elif dados_movimentacao['tipo'] == 'entrada':
        novo_estoque = estoque_atual + quantidade_mov
    else:
        raise Exception("Tipo de movimentação inválido")
        
    if novo_estoque < 0:
        raise Exception("Estoque não pode ficar negativo")

    medicamento['quantidade_estoque'] = novo_estoque
    
    todos_medicamentos = med_repo.get_all()
    for i, med in enumerate(todos_medicamentos):
        if med['id'] == str(dados_movimentacao['id_medicamento']):
            todos_medicamentos[i] = medicamento
            break
    med_repo.update_all(todos_medicamentos)

    dados_movimentacao['id'] = db_base.gerar_id(db_base.MOVIMENTACOES_CSV)
    if 'data' not in dados_movimentacao:
        dados_movimentacao['data'] = datetime.now().isoformat()
        
    return mov_repo.add_new(dados_movimentacao)

def get_todas_movimentacoes():
    return mov_repo.get_all()