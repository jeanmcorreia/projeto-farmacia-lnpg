import repositories.db as db

FILE_PATH = db.MOVIMENTACOES_CSV

def get_all():
    return db.ler_tudo(FILE_PATH)

def add_new(movimentacao_data):
    db.adicionar_linha(FILE_PATH, movimentacao_data)
    return movimentacao_data