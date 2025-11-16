import repositories.db as db

FILE_PATH = db.VENDAS_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def find_by_id(id):
    return db.procurar_por_id(FILE_PATH, id)

def add_new(venda_data):
    db.adicionar_linha(FILE_PATH, venda_data)
    return venda_data