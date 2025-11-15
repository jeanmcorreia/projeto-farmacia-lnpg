import csv
import os

DB_DIR = 'db'

CLIENTES_CSV = os.path.join(DB_DIR, 'clientes.csv')
FUNCIONARIOS_CSV = os.path.join(DB_DIR, 'funcionarios.csv')
MEDICAMENTOS_CSV = os.path.join(DB_DIR, 'medicamentos.csv')
MOVIMENTACOES_CSV = os.path.join(DB_DIR, 'movimentacoes.csv')
VENDAS_CSV = os.path.join(DB_DIR, 'vendas.csv')
ITENS_VENDA_CSV = os.path.join(DB_DIR, 'itens_venda.csv')

HEADERS = {
    CLIENTES_CSV: ['id', 'nome', 'cpf', 'telefone', 'email'],
    FUNCIONARIOS_CSV: ['id', 'nome', 'cpf', 'cargo', 'email'],
    MEDICAMENTOS_CSV: ['id', 'nome', 'fabricante', 'preco_unitario', 'quantidade_estoque', 'validade'],
    MOVIMENTACOES_CSV: ['id', 'id_medicamento', 'tipo', 'quantidade', 'data', 'id_funcionario'],
    VENDAS_CSV: ['id', 'id_cliente', 'id_funcionario', 'data_venda', 'valor_total'],
    ITENS_VENDA_CSV: ['id', 'id_venda', 'id_medicamento', 'quantidade', 'preco_unitario_momento'],
}


def ensure_db_dir():
    os.makedirs(DB_DIR, exist_ok=True)


def inicializar_db():
    """Inicializa banco de dados criando arquivos CSV com headers"""
    ensure_db_dir()
    for filepath, headers in HEADERS.items():
        if not os.path.exists(filepath):
            _escrever_csv(filepath, [], headers)


def _ler_csv(filepath):
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def _escrever_csv(filepath, data, headers):
    ensure_db_dir()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def _gerar_proximo_id(filepath):
    dados = _ler_csv(filepath)
    if not dados:
        return 1
    ids_validos = [int(item['id']) for item in dados if 'id' in item and str(item['id']).isdigit()]
    return max(ids_validos) + 1 if ids_validos else 1


def ler_tudo(filepath):
    return _ler_csv(filepath)


def digitar_tudo(filepath, data):
    headers = HEADERS.get(filepath)
    if headers is None:
        raise ValueError(f"Unknown headers for {filepath}")
    _escrever_csv(filepath, data, headers)


def adicionar_linha(filepath, row):
    dados = _ler_csv(filepath)
    dados.append(row)
    digitar_tudo(filepath, dados)


def ler_medicamentos():
    return ler_tudo(MEDICAMENTOS_CSV)


def escrever_medicamentos(data):
    digitar_tudo(MEDICAMENTOS_CSV, data)


def ler_vendas():
    return ler_tudo(VENDAS_CSV)


def digitar_vendas(data):
    digitar_tudo(VENDAS_CSV, data)


def ler_itens_venda():
    return ler_tudo(ITENS_VENDA_CSV)


def digitar_itens_venda(data):
    digitar_tudo(ITENS_VENDA_CSV, data)


def procurar_por_id(filepath, id_value):
    for item in _ler_csv(filepath):
        if item.get('id') == str(id_value):
            return item
    return None


def procurar_itens_por_venda(id_venda):
    itens = _ler_csv(ITENS_VENDA_CSV)
    return [i for i in itens if i.get('id_venda') == str(id_venda)]
