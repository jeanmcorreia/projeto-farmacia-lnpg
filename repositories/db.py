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
    """Garante que o diretório 'db' exista."""
    os.makedirs(DB_DIR, exist_ok=True)


def inicializar_db():
    """Inicializa o banco de dados criando arquivos CSV com headers, se não existirem."""
    ensure_db_dir()
    for filepath, headers in HEADERS.items():
        if not os.path.exists(filepath):
            _escrever_csv(filepath, [], headers)


def _ler_csv(filepath):
    """Função helper privada para ler um CSV."""
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def _escrever_csv(filepath, data, headers):
    """Função helper privada para escrever em um CSV."""
    ensure_db_dir()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def _gerar_proximo_id(filepath):
    """Função helper privada para gerar um novo ID."""
    dados = _ler_csv(filepath)
    if not dados:
        return 1
    ids_validos = [int(item['id']) for item in dados if 'id' in item and str(item['id']).isdigit()]
    return max(ids_validos) + 1 if ids_validos else 1


def ler_tudo(filepath):
    """Lê todas as linhas de um arquivo CSV."""
    return _ler_csv(filepath)


def digitar_tudo(filepath, data):
    """Sobrescreve um arquivo CSV com novos dados."""
    headers = HEADERS.get(filepath)
    if headers is None:
        raise ValueError(f"Headers desconhecidos para {filepath}")
    _escrever_csv(filepath, data, headers)


def adicionar_linha(filepath, row):
    """Adiciona uma nova linha a um arquivo CSV (sem gerar ID)."""
    dados = _ler_csv(filepath)
    dados.append(row)
    digitar_tudo(filepath, dados)


def procurar_por_id(filepath, id_value):
    """Procura um item por ID em qualquer arquivo CSV."""
    for item in _ler_csv(filepath):
        if item.get('id') == str(id_value):
            return item
    return None

def gerar_id(filepath):
    """Expõe a função de gerar ID para os services usarem."""
    return _gerar_proximo_id(filepath)