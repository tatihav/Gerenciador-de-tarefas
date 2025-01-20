import os
import json
from datetime import datetime

# Função para carregar tarefas
def carregar_tarefas():
    if os.path.exists('tarefas.json'):
        with open('tarefas.json', 'r') as arquivo:
            return json.load(arquivo)
    else:
        return []

# Exibe todas as tarefas
def listar_tarefas(tarefas):
    print("\nTarefas pendentes:")
    tarefas_pendentes = [t for t in tarefas if not t['concluida']]
    tarefas_pendentes = sorted(tarefas_pendentes, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

    for tarefa in tarefas_pendentes:
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Data: {tarefa['data']}")

    print("\nTarefas concluídas:")
    tarefas_concluidas = [t for t in tarefas if t['concluida']]
    tarefas_concluidas = sorted(tarefas_concluidas, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

    for tarefa in tarefas_concluidas:
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Data: {tarefa['data']}")

# Escreve e salva as tarefas
def salvar_tarefas(tarefas):
    with open('tarefas.json', 'w') as arquivo:
        json.dump(tarefas, arquivo, indent=4)

# Gerar ID
def gerar_id(tarefas):
    if tarefas:
        ultimo_id = max(tarefa['id'] for tarefa in tarefas)
        return ultimo_id + 1
    else:
        return 1

# Adicionar tarefas
def adicionar_tarefas(tarefas):
    print("\nAdicionar nova tarefa")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    data_input = input("Data de conclusão (dd/mm/aaaa): ")
    try:
        data_obj = datetime.strptime(data_input, '%d/%m/%Y')  # Converte string para datetime
        if data_obj.date() < datetime.now().date():  # Verifica se a data é no passado
            print("Data de conclusão não pode ser no passado.")
            return
        data = data_obj.strftime('%d/%m/%Y')  # Converte para string formatada
    except ValueError:
        print("Data em formato inválido. Utilize dd/mm/aaaa.")
        return

    tarefa = {
        'id': gerar_id(tarefas),
        'titulo': titulo,
        'descricao': descricao,
        'data': data,
        'concluida': False  # Chave corrigida para consistência
    }

    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    print("Tarefa inserida com sucesso!")

# Concluir tarefa
def concluir_tarefa(tarefas):
    try:
        id_tarefa = int(input("Digite o ID da tarefa para concluir: "))
        for tarefa in tarefas:
            if tarefa['id'] == id_tarefa:
                if tarefa['concluida']:
                    print("A tarefa já está concluída!")
                else:
                    tarefa['concluida'] = True
                    salvar_tarefas(tarefas)
                    print("Tarefa concluída com sucesso!")
                return
        print("Tarefa não encontrada!")
    except ValueError:
        print("ID inválido!")

# Remover tarefas
def remover_tarefa(tarefas):
    try:
        id_tarefa = int(input("Digite o ID da tarefa para remover: "))
        for tarefa in tarefas:
            if tarefa['id'] == id_tarefa:
                tarefas.remove(tarefa)
                salvar_tarefas(tarefas)
                print("Tarefa removida com sucesso!")
                return
        print("Tarefa não encontrada.")
    except ValueError:
        print("ID inválido.")

# Pesquisar tarefas
def pesquisar_tarefas(tarefas):
    termo = input("Digite o termo de pesquisa: ").lower()
    resultados = [t for t in tarefas if termo in t['titulo'].lower() or termo in t['descricao'].lower()]
    if resultados:
        print(f"\nTarefas que contêm '{termo}':")
        for tarefa in resultados:
            status = "Concluída" if tarefa['concluida'] else "Pendente"
            print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Status: {status}, Data: {tarefa['data']}")
    else:
        print("Nenhuma tarefa encontrada.")

# Ordenar tarefas por data
def ordenar_tarefas(tarefas):
    tarefas.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))
    salvar_tarefas(tarefas)
    print("Tarefas ordenadas por data de conclusão com sucesso!")

# Menu principal
def menu():
    print("=== GERENCIADOR DE TAREFAS ===")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Concluir Tarefa")
    print("4. Remover Tarefa")
    print("5. Pesquisar Tarefas")
    print("6. Ordenar Tarefas por Data")
    print("7. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

# Loop principal
def main():
    tarefas = carregar_tarefas()
    while True:
        opcao = menu()

        if opcao == '1':
            adicionar_tarefas(tarefas)
        elif opcao == '2':
            listar_tarefas(tarefas)
        elif opcao == '3':
            concluir_tarefa(tarefas)
        elif opcao == '4':
            remover_tarefa(tarefas)
        elif opcao == '5':
            pesquisar_tarefas(tarefas)
        elif opcao == '6':
            ordenar_tarefas(tarefas)
        elif opcao == '7':
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    main()
