import repositories.medicamento_db as med_repo
import repositories.db as db_base

def get_todos_medicamentos():
    return med_repo.get_all()

def get_medicamento_por_id(id_medicamento):
    return med_repo.find_by(id_medicamento)

def criar_medicamento(dados):
    dados['id'] = db_base.gerar_id(db_base.MEDICAMENTOS_CSV)
    return med_repo.add_new(dados)

def atualizar_medicamento(id, dados):
    medicamento = med_repo.find_by_id(id)
    if not medicamento:
        return None
    
    medicamento.update(dados)
    

    todos_medicamentos = med_repo.get_all()
    for i, med in enumerate(todos_medicamentos):
        if med['id'] == str(id):
            todos_medicamentos[i] = medicamento
            break


    med_repo.update_all(todos_medicamentos)
    return medicamento