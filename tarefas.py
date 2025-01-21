import os
import json
from datetime import datetime
import csv

# Função para carregar tarefas
def carregar_tarefas():
    if os.path.exists('tarefas.json'):
        with open('tarefas.json', 'r') as arquivo:
            return json.load(arquivo)
    else:
        return []

# Listar todas as tarefas
def listar_tarefas(tarefas):
    print("\nTarefas pendentes:")
    tarefas_pendentes = [t for t in tarefas if not t['concluida']]
    tarefas_pendentes = sorted(tarefas_pendentes, key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

    for tarefa in tarefas_pendentes:
        data_obj = datetime.strptime(tarefa['data'], '%d/%m/%Y')
        status_atrasado = " [ATRASADA]" if data_obj.date() < datetime.now().date() else""
        print(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Data: {tarefa['data']}{status_atrasado}")


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

#Editar tarefas
def editar_tarefas(tarefas):
    try:
        id_tarefa = int(input("Digite o ID da tarefa a ser editada: "))
        for tarefa in tarefas:
            if tarefa['id'] == id_tarefa:
                print(f"Editar Tarefa ID {id_tarefa}:")
                novo_titulo = input(f"Novo Título (atual:{tarefa['titulo']}): ") or tarefa['titulo']
                nova_descricao = input(f"Nova descrição (atual: {tarefa['descricao']}): ") or tarefa['descricao']
                nova_data = input(f"Nova data de conclusão (atual: {tarefa['data']}, formato dd/mm/aaaa): ") or tarefa['data']
                try:
                    data_obj = datetime.strptime(nova_data, '%d/%m/%Y')
                    if data_obj.date() < datetime.now().date():
                        print("Data de conclusão não pode ser no passado.")
                        return
                    tarefa['data'] = data_obj.strftime('%d/%m/%Y')
                except ValueError:
                    print("Data em formato inválido.")
                    return
                tarefa['titulo'] = novo_titulo
                tarefa['descricao'] = nova_descricao
                salvar_tarefas(tarefas)
                print("Tarefa editada com sucesso!")
                return
        print("Tarefa não encontrada!")
    except ValueError:
        print("ID inválido.")
        

# Exportar CSV
def exportar_tarefas(tarefas):
    try:
        with open('tarefas_exportadas.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
            campos = ['ID', 'Título', 'Descrição', 'Data de conclusão', 'Concluída']
            escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
            escritor.writeheader()
            for tarefa in tarefas:
                escritor.writerow({
                    'ID': tarefa['id'],
                    'Título': tarefa['titulo'],
                    'Descrição': tarefa['descricao'],
                    'Data de conclusão': tarefa['data'],
                    'Concluída': 'Sim' if tarefa['concluida'] else 'Não'
                })
            print("Tarefas exportadas com sucesso para 'tarefas_exportadas.csv'.")
    except Exception as e:
        print(f"Ocorreu um erro ao exportar as tarefas: {e}")
#Importar CSV
def importar_tarefas(tarefas):
    nome_arquivo = input("Digite o nome do arquivo CSV para importar: ")
    try:
        with open(nome_arquivo, 'r') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                try:
                                  
                    # Verifica se todas as colunas estão presentes
                    if not all(campo in linha for campo in ['Título', 'Descrição', 'Data de Conclusão', 'Concluída']):
                        print("Formato de arquivo inválido. Certifique-se de que o CSV contém as colunas corretas.")
                        return
                    # Valida os dados de cada tarefa
                    tarefa = {
                        'id': gerar_id(tarefas),
                        'titulo': linha['Título'],
                        'descricao': linha['Descrição'],
                        'data': linha['Data de Conclusão'],
                        'concluida': True if linha['Concluída'].strip().lower() == 'sim' else False
                    }
                    # Verifica se a data está no formato correto
                    datetime.strptime(tarefa['data'], '%d/%m/%Y')  # Gera um erro se o formato estiver inválido
                    tarefas.append(tarefa)
                except ValueError as ve:
                    print(f"Erro nos dados da tarefa: {ve}. Certifique-se de que as datas estão no formato dd/mm/aaaa.")
                    return

            salvar_tarefas(tarefas)
            print(f"Tarefas importadas com sucesso do arquivo '{nome_arquivo}'.")
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f" Ocorreu um erro ao importar as tarefas: {e}")


                                    

# Menu principal
def menu():
    print("=== GERENCIADOR DE TAREFAS ===")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Concluir Tarefa")
    print("4. Remover Tarefa")
    print("5. Pesquisar Tarefas")
    print("6. Ordenar Tarefas por Data")
    print("7. Editar Tarefa")
    print("8. Exportar para CSV")
    print("9. Importar Tarefas de CSV")
    print("10. Sair")
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
            editar_tarefas(tarefas)
       
        elif opcao == '8':
            exportar_tarefas(tarefas)
        elif opcao == '9':
            importar_tarefas(tarefas)

        elif opcao == '10':
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    main()
