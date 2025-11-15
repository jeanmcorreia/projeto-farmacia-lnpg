from datetime import datetime
import repositories.db as repo


def get_medicamento_por_id(id_medicamento):
    """Busca medicamento por ID"""
    return repo.procurar_por_id(repo.MEDICAMENTOS_CSV, id_medicamento)


def add_movimentacao(dados_movimentacao):
    """Adiciona movimento de estoque (entrada/saída)"""
    medicamento = get_medicamento_por_id(dados_movimentacao['id_medicamento'])
    if medicamento:
        estoque_atual = int(medicamento.get('quantidade_estoque', 0))
        quantidade_mov = int(dados_movimentacao['quantidade'])

        novo_estoque = estoque_atual
        if dados_movimentacao['tipo'] == 'saida':
            novo_estoque = estoque_atual - quantidade_mov
        elif dados_movimentacao['tipo'] == 'entrada':
            novo_estoque = estoque_atual + quantidade_mov

        todos_medicamentos = repo.ler_medicamentos()
        for med in todos_medicamentos:
            if med['id'] == str(dados_movimentacao['id_medicamento']):
                med['quantidade_estoque'] = novo_estoque
                break
        repo.escrever_medicamentos(todos_medicamentos)

    todas_mov = repo._ler_csv(repo.MOVIMENTACOES_CSV)
    dados_movimentacao['id'] = repo._gerar_proximo_id(repo.MOVIMENTACOES_CSV)
    todas_mov.append(dados_movimentacao)
    repo._escrever_csv(repo.MOVIMENTACOES_CSV, todas_mov, repo.HEADERS[repo.MOVIMENTACOES_CSV])

    return dados_movimentacao


def realizar_venda(dados_venda):
    '''
    Realiza uma venda: valida estoque, calcula preço, registra venda e movimentação
    Retorna (venda_dict, 201) ou ({"erro": "..."}, status_code)
    '''
    try:
        itens_processados = []
        valor_total_calculado = 0.0

        for item_req in dados_venda['itens']:
            medicamento = get_medicamento_por_id(item_req['id_medicamento'])

            if not medicamento:
                return {"erro": f"Medicamento com ID {item_req['id_medicamento']} não encontrado."}, 404
            
            estoque_atual = int(medicamento.get('quantidade_estoque', 0))
            preco_unit = float(medicamento.get('preco_unitario', 0.0))

            if estoque_atual < item_req['quantidade']:
                return {"erro": f"Estoque insuficiente para {medicamento['nome']}. Restam {estoque_atual} unidades."}, 400
            
            itens_processados.append({
                "id_medicamento": item_req['id_medicamento'],
                "quantidade": item_req['quantidade'],
                "preco_unitario_momento": preco_unit
            })
            valor_total_calculado += preco_unit * item_req['quantidade']

        id_nova_venda = repo._gerar_proximo_id(repo.VENDAS_CSV)
        nova_venda_dados = {
            'id': id_nova_venda,
            'id_cliente': dados_venda['id_cliente'],
            'id_funcionario': dados_venda['id_funcionario'],
            'data_venda': datetime.now().isoformat(),
            'valor_total': round(valor_total_calculado, 2)
        }

        todas_vendas = repo.ler_vendas()
        todas_vendas.append(nova_venda_dados)
        repo.digitar_vendas(todas_vendas)

        todos_itens_venda = repo.ler_itens_venda()
        for item in itens_processados:
            novo_item_venda_id = repo._gerar_proximo_id(repo.ITENS_VENDA_CSV)
            todos_itens_venda.append({
                'id': novo_item_venda_id,
                'id_venda': id_nova_venda,
                'id_medicamento': item['id_medicamento'],
                'quantidade': item['quantidade'],
                'preco_unitario_momento': item['preco_unitario_momento']
            })

            add_movimentacao({
                'id_medicamento': item['id_medicamento'],
                'tipo': 'saida',
                'quantidade': item['quantidade'],
                'data': datetime.now().isoformat(),
                'id_funcionario': dados_venda['id_funcionario']
            })

        repo.digitar_itens_venda(todos_itens_venda)

        nova_venda_dados['itens'] = itens_processados
        return nova_venda_dados, 201
    
    except Exception as e:
        print(f"Erro ao realizar_venda: {e}")
        return {"erro": f"Ocorreu um erro interno no servidor: {e}"}, 500


def get_todas_vendas():
    """Retorna todas as vendas"""
    return repo.ler_vendas()


def get_venda_por_id(id_venda):
    """Busca venda por ID incluindo itens associados"""
    venda = repo.procurar_por_id(repo.VENDAS_CSV, id_venda)
    
    if not venda:
        return None
    
    itens = repo.procurar_itens_por_venda(id_venda)
    venda['itens'] = itens
    return venda