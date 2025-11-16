import repositories.cliente_db as cliente_repo
import repositories.db as db_base

def get_todos_clientes():
    return cliente_repo.get_all()

def get_cliente_por_id(id_cliente):
    return cliente_repo.find_by_id(id_cliente)

def criar_cliente(dados):    
    dados['id'] = db_base.gerar_id(db_base.CLIENTES_CSV)
    return cliente_repo.add_new(dados)

def atualizar_cliente(id, dados):
    cliente = cliente_repo.find_by_id(id)
    if not cliente:
        return None
    
    cliente.update(dados)
    
    todos_clientes = cliente_repo.get_all()
    for i, cli in enumerate(todos_clientes):
        if cli['id'] == str(id):
            todos_clientes[i] = cliente
            break
            
    cliente_repo.update_all(todos_clientes)
    return cliente

def deletar_cliente(id):
    todos_clientes = cliente_repo.get_all()
    novos_dados = [c for c in todos_clientes if c['id'] != str(id)]
    
    if len(novos_dados) < len(todos_clientes):
        cliente_repo.update_all(novos_dados)
        return True
    return False