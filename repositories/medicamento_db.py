import repositories.db as db
from datetime import date

FILE_PATH = db.MEDICAMENTOS_CSV

def _converter_tipos(med):
    if isinstance(med.get("validade"), str):
        med["validade"] = date.fromisoformat(med["validade"])
    
    med["preco_unitario"] = float(med["preco_unitario"])
    med["quantidade_estoque"] = int(med["quantidade_estoque"])
    
    return med

def _preparar_para_salvar(med):
    if isinstance(med.get("validade"), date):
        med["validade"] = med["validade"].isoformat()
    
    med["preco_unitario"] = str(med["preco_unitario"])
    med["quantidade_estoque"] = str(med["quantidade_estoque"])
    
    return med

def get_all():
    dados = db.ler_tudo(FILE_PATH)
    return [_converter_tipos(m) for m in dados]

def find_by_id(id):
    med = db.procurar_por_id(FILE_PATH, id)
    if med:
        return _converter_tipos(med)
    return None

def add_new(medicamento_data):
    db.adicionar_linha(FILE_PATH, _preparar_para_salvar(medicamento_data))
    return medicamento_data

def update_all(medicamentos_data):
    dados_convertidos = [_preparar_para_salvar(m) for m in medicamentos_data]
    db.digitar_tudo(FILE_PATH, dados_convertidos)

def delete(id):
    todos = get_all()
    novos = [m for m in todos if m["id"] != str(id)]
    
    if len(novos) < len(todos):
        update_all(novos)
        return True
    return False