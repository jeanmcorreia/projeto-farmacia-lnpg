import repositories.funcionario_db as func_repo
import repositories.db as db_base

def get_todos_funcionarios():
    return func_repo.get_all()

def get_funcionario_por_id(id_funcionario):
    return func_repo.find_by_id(id_funcionario)

def criar_funcionario(dados):
    dados['id'] = db_base.gerar_id(db_base.FUNCIONARIOS_CSV)
    return func_repo.add_new(dados)

def atualizar_funcionario(id, dados):
    funcionario = func_repo.find_by_id(id)
    if not funcionario:
        return None
    
    funcionario.update(dados)
    
    todos_funcionarios = func_repo.get_all()
    for i, func in enumerate(todos_funcionarios):
        if func['id'] == str(id):
            todos_funcionarios[i] = funcionario
            break
            
    func_repo.update_all(todos_funcionarios)
    return funcionario

def deletar_funcionario(id):
    todos_funcionarios = func_repo.get_all()
    novos_dados = [f for f in todos_funcionarios if f['id'] != str(id)]
    
    if len(novos_dados) < len(todos_funcionarios):
        func_repo.update_all(novos_dados)
        return True
    return False