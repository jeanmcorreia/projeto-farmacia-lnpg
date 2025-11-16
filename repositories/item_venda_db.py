import repositories.db as db

FILE_PATH = db.ITENS_VENDA_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def add_new(item_venda_data):
    db.adicionar_linha(FILE_PATH, item_venda_data)
    return item_venda_data

def find_by_id(id_venda):
    todos_itens = db.ler_tudo(FILE_PATH)
    return [item for item in todos_itens if item.get('id_venda') == str(id_venda)]