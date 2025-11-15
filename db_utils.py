import csv
import os
from datetime import datetime

DB_DIR = 'db'

CLIENTES_CSV = os.path.join(DB_DIR, 'clientes.csv')
HEADERS_CLIENTE = ['id', 'nome', 'cpf', 'telefone', 'email']
FUNCIONARIOS_CSV = os.path.join(DB_DIR, 'funcionarios.csv')
HEADERS_FUNCIONARIO = ['id', 'nome', 'cpf', 'cargo', 'email']
MEDICAMENTOS_CSV = os.path.join(DB_DIR, 'medicamentos.csv')
HEADERS_MEDICAMENTO = ['id', 'nome', 'fabricante', 'preco_unitario', 'quantidade_estoque', 'validade']
MOVIMENTACOES_CSV = os.path.join(DB_DIR, 'movimentacoes.csv')
HEADERS_MOVIMENTACAO = ['id', 'id_medicamento', 'tipo', 'quantidade', 'data', 'id_funcionario']
VENDAS_CSV = os.path.join(DB_DIR, 'vendas.csv')
HEADERS_VENDA = ['id', 'id_cliente', 'id_funcionario', 'data_venda', 'valor_total']
ITENS_VENDA_CSV = os.path.join(DB_DIR, 'itens_venda.csv')
HEADERS_ITENS_VENDA = ['id', 'id_venda', 'id_medicamento', 'quantidade', 'preco_unitario_momento']

ARQUIVOS_CSV_HEADERS = {
    CLIENTES_CSV: HEADERS_CLIENTE,
    FUNCIONARIOS_CSV: HEADERS_FUNCIONARIO,
    MEDICAMENTOS_CSV: HEADERS_MEDICAMENTO,
    MOVIMENTACOES_CSV: HEADERS_MOVIMENTACAO,
    VENDAS_CSV: HEADERS_VENDA,
    ITENS_VENDA_CSV: HEADERS_ITENS_VENDA
}

def inicializar_db():
    os.makedirs(DB_DIR, exist_ok=True)
    for filepath, headers in ARQUIVOS_CSV_HEADERS.items():
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def _ler_csv(filepath):
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []
    

def _escrever_csv(filepath, data, headers):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def _gerar_proximo_id(filepath):
    dados = _ler_csv(filepath)
    if not dados:
        return 1
    ids_validos = [int(item['id']) for item in dados if 'id' in item and item['id'].isdigit()]
    return max(ids_validos) + 1 if ids_validos else 1

# FUNÇÕES KELVEN
# CODIGO CRUD DE CLIENTE E FUNCIONARIO


# FUNÇÕES JEAN
# MOCKS FUNCIONAIS

# MOCKS DE TESTE (SUBSTITUIR POR CODIGOS REAIS DEPOIS)
def get_medicamento_por_id(id_medicamento):
    todos = _ler_csv(MEDICAMENTOS_CSV)
    for item in todos:
        if item['id'] == str(id_medicamento):
            return item
    return None

def add_movimentacao(dados_movimentacao):
    medicamento = get_medicamento_por_id(dados_movimentacao['id_medicamento'])
    if medicamento:
        estoque_atual = int(medicamento.get('quantidade_estoque, 0'))
        quantidade_mov = int(dados_movimentacao['quantidade'])

        novo_estoque = estoque_atual
        if dados_movimentacao['tipo'] == 'saida':
            novo_estoque = estoque_atual - quantidade_mov
        elif dados_movimentacao['tipo'] == 'entrada':
            novo_estoque = estoque_atual + quantidade_mov


        todos_medicamentos = _ler_csv(MEDICAMENTOS_CSV)
        for med in todos_medicamentos:
            if med['id'] == str(dados_movimentacao['id_medicamento']):
                med['quantidade_estoque'] = novo_estoque
                break
        _escrever_csv(MEDICAMENTOS_CSV, todos_medicamentos, HEADERS_MEDICAMENTO)

    
    todas_mov = _ler_csv(MOVIMENTACOES_CSV)
    dados_movimentacao['id'] = _gerar_proximo_id(MOVIMENTACOES_CSV)
    todas_mov.append(dados_movimentacao)
    _escrever_csv(MOVIMENTACOES_CSV, todas_mov, HEADERS_MOVIMENTACAO)

    return dados_movimentacao

''' FIM DO BLOCO DE SUBSTITUICAO DO JEAN '''

def get_todas_vendas():
    return _ler_csv(VENDAS_CSV)


def get_venda_por_id(id_venda):
    venda_encontrada = None
    vendas = _ler_csv(VENDAS_CSV)
    for v in vendas:
        if v['id'] == str(id_venda):
            venda_encontrada = v
            break

    if not venda_encontrada:
        return None
    
    itens = _ler_csv(ITENS_VENDA_CSV)
    itens_da_venda = [item for item in itens if item['id_venda'] == str(id_venda)]

    venda_encontrada['itens'] = itens_da_venda
    return venda_encontrada

def realizar_venda(dados_venda):
    '''
    Chama as mocks pra validar estoque, calcular preço e registrar venda
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

        id_nova_venda = _gerar_proximo_id(VENDAS_CSV)
        nova_venda_dados = {
            'id': id_nova_venda,
            'id_cliente': dados_venda['id_cliente'],
            'id_funcionario': dados_venda['id_funcionario'],
            'data_venda': datetime.now().isoformat(),
            'valor_total': round(valor_total_calculado, 2)
        }

        todas_vendas = _ler_csv(VENDAS_CSV)
        todas_vendas.append(nova_venda_dados)
        _escrever_csv(VENDAS_CSV, todas_vendas, HEADERS_VENDA)


        todos_itens_venda = _ler_csv(ITENS_VENDA_CSV)
        for item in itens_processados:
            novo_item_venda_id = _gerar_proximo_id(ITENS_VENDA_CSV)
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

        _escrever_csv(ITENS_VENDA_CSV, todos_itens_venda, HEADERS_ITENS_VENDA)

        nova_venda_dados['itens'] = itens_processados
        return nova_venda_dados, 201
    
    except Exception as e:
        print(f"Erro ao realizar_venda: {e}")
        return {"erro": f"Ocorreu um erro interno no servidor: {e}"}, 500
    