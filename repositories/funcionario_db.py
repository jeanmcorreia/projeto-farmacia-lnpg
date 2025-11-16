import repositories.db as db

FILE_PATH = db.FUNCIONARIOS_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def find_by_id(id):
    return db.procurar_por_id(FILE_PATH, id)

def add_new(funcionario_data):
    db.adicionar_linha(FILE_PATH, funcionario_data)
    return funcionario_data

def update_all(funcionarios_data):
    db.digitar_tudo(FILE_PATH, funcionarios_data)