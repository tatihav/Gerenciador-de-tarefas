import os
import json

# função para acrregar tarefas

def carregar_tarefas():
    if os.path.exists('tarefas.json'):
        with open('tarefas.json', 'r') as arquivo:
            return json.load(arquivo)
    return[]
    
    # exibe todas as tarefas
def listar_tarefas(tarefas):
    print("Tarefas:")
    for tarefa in tarefas:
        status = "Concluída" if tarefa['status'] else "Pendente"
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Status: {status}")

#Escreve e salva as tarefas
def salvar_tarefas(tarefas):
    with open('tarefas.json', 'w') as arquivo:
        json.dump(tarefas, arquivo, indent=4)

# gerar id
def gerar_id(tarefas):
    if tarefas:
        return tarefas[-1]['id'] + 1

#Adicionar tarefas
def adicionar_tarefas(tarefas):
    print("Adicionar nova tarefa")
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    tarefa = {
        'id': gerar_id(tarefas),
        'titulo': titulo,
        'descricao': descricao,
        'status': False
    }
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    print("Tarefa inserida com sucesso!")
#concluir tarefa
def concluir_tarefa(tarefas):
    try: 
        id_tarefa = int(input("Digite o ID da tarefa para concluir: "))
        for tarefa in tarefas:
            if tarefa['id'] == id_tarefa:
                if tarefa['status']:
                    print("A tarefa já está concluida!")
                else:
                     tarefa['status'] = True
                     salvar_tarefas(tarefas)
                     print("Tarefa concluída com sucesso!")
                return
        print("Tarefa não encontrada!")
    except ValueError:
        print("ID inválido!")

# remover tarefas
def remover_tarefa(tarefas):
    try:
        id_tarefa = int(input("Digite o ID da tarefa para Remover: "))
        for tarefa in tarefas:
            if tarefa['id'] == id_tarefa:
                tarefas.remove(tarefa)
                salvar_tarefas(tarefas)
                print("Tarefa removida com sucesso!")
                return
        print("Tarefa não encontrada")
    except ValueError:
        print("ID inválido.")



# menu principal
def menu():
    print("=== GERENCIADOR DE TAREFAS ===")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Concluir Tarefa")
    print("4. Remover Tarefa")
    print("5. Sair")
    return input("Escolha uma opção: ")

#Loop açoes 
def main():
    tarefas = carregar_tarefas()
    while True:
        opcao = menu()

        if opcao == '1':
            adicionar_tarefas(tarefas)
        elif  opcao == '2':
            listar_tarefas(tarefas)
        elif opcao == '3':
            concluir_tarefa(tarefas)
            
        elif opcao == '4':
            remover_tarefa(tarefas)
        elif opcao == '5':
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!")


if __name__=='__main__':
    main()