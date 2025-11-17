import repositories.db as db

FILE_PATH = db.MEDICAMENTOS_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def find_by_id(id):
    return db.procurar_por_id(FILE_PATH, id)

def add_new(medicamento_data):
    db.adicionar_linha(FILE_PATH, medicamento_data)
    return medicamento_data

def update_all(medicamentos_data):
    db.digitar_tudo(FILE_PATH, medicamentos_data)

def delete(id):
    todos = get_all()
    novos_dados = [med for med in todos if med['id'] != str(id)]
    
    if len(novos_dados) < len(todos):
        update_all(novos_dados)
        return True
    return False