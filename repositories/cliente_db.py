import repositories.db as db

FILE_PATH = db.CLIENTES_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def find_by_id(id):
    return db.procurar_por_id(FILE_PATH, id)

def add_new(cliente_data):
    db.adicionar_linha(FILE_PATH, cliente_data)
    return cliente_data

def update_all(clientes_data):
    db.digitar_tudo(FILE_PATH, clientes_data)