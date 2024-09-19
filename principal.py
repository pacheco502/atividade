from atividade import Tarefa
import os
from tabulate import tabulate
from datetime import datetime

# Funções do menu
def menu():
    os.system("cls")
    print("========== Gerenciador de Tarefas ==========")
    print("1 - Inserir tarefa")
    print("2 - Alterar tarefa")
    print("3 - Excluir tarefa")
    print("4 - Consultar tarefa")
    print("5 - Marcar tarefa como concluída")
    print("6 - Listar todas as tarefas")
    print("7 - Filtrar tarefas por status")
    print("8 - Listar tarefas vencidas")
    print("9 - Sair")
    print("============================================")
    
    opcao = int(input("Digite a opção desejada: "))
    
    match opcao:
        case 1:
            inserir()
        case 2:
            alterar()
        case 3:
            excluir()
        case 4:
            consultar()
        case 5:
            concluir_tarefa()
            
        case 6:
            listar_todas_as_tarefas()
        case 7:
            filtrar_por_status()
        case 8:
            listar_vencidas()
        case 9:
            exit()
        case _:
            print("Opção inválida")
            menu()

# Inserir tarefa
def inserir():
    os.system("cls")
    print("========== INSERIR TAREFA ==========")
    titulo = input("Digite o título da tarefa: ")
    descricao = input("Digite a descrição da tarefa: ")
    categoria = input("Digite a categoria da tarefa: ")
    status = "não concluída"
    data_prazo = input("Digite o prazo (AAAA-MM-DD): ")
    nota = input("Digite a nota da tarefa (ou deixe em branco para nenhuma nota): ")

    objTarefa = Tarefa()
    
    if objTarefa.inserir(titulo, descricao, categoria, status, data_prazo, nota):
        print("Tarefa inserida com sucesso!")
    else:
        print("Erro ao inserir tarefa!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Alterar tarefa
def alterar():
    os.system("cls")
    print("========== ALTERAR TAREFA ==========")
    id_tarefa = int(input("Digite o ID da tarefa: "))
    
    objTarefa = Tarefa()
    
    # Consultar a tarefa para exibir os dados atuais
    tarefa = objTarefa.consultar(id_tarefa=id_tarefa)
    
    if not tarefa:
        print("Tarefa não encontrada!")
        input("Aperte ENTER para voltar...")
        menu()
        return
    
    # Mostrar detalhes da tarefa
    colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
    tabela = tabulate(tarefa, headers=colunas, tablefmt="grid")
    print(tabela)
    
    # Perguntar quais campos deseja alterar
    alterar_titulo = input("Deseja alterar o título? (s/n): ").lower() == 's'
    alterar_descricao = input("Deseja alterar a descrição? (s/n): ").lower() == 's'
    alterar_categoria = input("Deseja alterar a categoria? (s/n): ").lower() == 's'
    alterar_status = input("Deseja alterar o status? (s/n): ").lower() == 's'
    alterar_prazo = input("Deseja alterar o prazo? (s/n): ").lower() == 's'
    alterar_nota = input("Deseja alterar a nota? (s/n): ").lower() == 's'
    
    # Coletar novos valores
    titulo = input("Novo título: ") if alterar_titulo else None
    descricao = input("Nova descrição: ") if alterar_descricao else None
    categoria = input("Nova categoria: ") if alterar_categoria else None
    status = input("Novo status: ") if alterar_status else None
    prazo = input("Novo prazo (AAAA-MM-DD): ") if alterar_prazo else None
    nota = input("Nova nota: ") if alterar_nota else None
    
    # Atualizar a tarefa
    if objTarefa.alterar(id_tarefa, titulo, descricao, categoria, status, prazo, nota):
        print("Tarefa alterada com sucesso!")
    else:
        print("Erro ao alterar tarefa!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Excluir tarefa
def excluir():
    os.system("cls")
    print("========== EXCLUIR TAREFA ==========")
    id_tarefa = int(input("Digite o ID da tarefa: "))
    
    objTarefa = Tarefa()
    
    if objTarefa.excluir(id_tarefa):
        print("Tarefa excluída com sucesso!")
    else:
        print("Erro ao excluir tarefa!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Consultar tarefa por ID ou título
def consultar():
    os.system("cls")
    print("========== CONSULTAR TAREFA ==========")
    consulta_tipo = input("Deseja consultar por (1) ID ou (2) Título? ")
    
    objTarefa = Tarefa()
    
    if consulta_tipo == '1':
        id_tarefa = int(input("Digite o ID da tarefa: "))
        resultado = objTarefa.consultar(id_tarefa=id_tarefa)
    elif consulta_tipo == '2':
        titulo = input("Digite o título da tarefa: ")
        resultado = objTarefa.consultar(titulo=titulo)
    else:
        print("Opção inválida")
        input("Aperte ENTER para voltar...")
        menu()
        return
    
    if resultado:
        colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
        tabela = tabulate(resultado, headers=colunas, tablefmt="grid")
        print(tabela)
    else:
        print("Nenhuma tarefa encontrada!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Marcar tarefa como concluída
def concluir_tarefa():
    os.system("cls")
    print("========== MARCAR TAREFA COMO CONCLUÍDA ==========")
    id_tarefa = int(input("Digite o ID da tarefa: "))
    
    objTarefa = Tarefa()
    
    # Consultar a tarefa pelo ID
    tarefa = objTarefa.consultar(id_tarefa=id_tarefa)
    
    if not tarefa:
        print("Tarefa não encontrada!")
        input("Aperte ENTER para voltar...")
        menu()
        return
    
    # Mostrar detalhes da tarefa
    colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
    tabela = tabulate(tarefa, headers=colunas, tablefmt="grid")
    print(tabela)
    
    # Verificar se a tarefa já está concluída
    status_atual = tarefa[0][4]  # A coluna de status está na posição 4
    if status_atual.lower() == 'concluída':
        print("A tarefa já está marcada como concluída!")
    else:
        confirmar = input("Deseja marcar essa tarefa como concluída? (s/n): ")
        if confirmar.lower() == 's':
            # Coletar todos os dados necessários para a atualização
            titulo = tarefa[0][1]
            descricao = tarefa[0][2]
            categoria = tarefa[0][3]
            data_prazo = tarefa[0][5]
            nota = tarefa[0][6]
            
            # Atualizar a tarefa com novos dados
            if objTarefa.alterar(id_tarefa, titulo, descricao, categoria, "Concluída", data_prazo, nota):
                print("Tarefa marcada como concluída!")
            else:
                print("Erro ao marcar tarefa como concluída!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Listar todas as tarefas
def listar_todas_as_tarefas():
    os.system("cls")
    print("========== LISTAR TODAS AS TAREFAS ==========")
    
    objTarefa = Tarefa()
    resultado = objTarefa.consultar()
    
    if resultado:
        colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
        tabela = tabulate(resultado, headers=colunas, tablefmt="grid")
        print(tabela)
    else:
        print("Nenhuma tarefa encontrada!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Filtrar tarefas por status
def filtrar_por_status():
    os.system("cls")
    print("========== FILTRAR TAREFAS POR STATUS ==========")
    status = input("Digite o status (concluída/não concluída): ")
    
    objTarefa = Tarefa()
    resultado = objTarefa.consultar_por_status(status)
    
    if resultado:
        colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
        tabela = tabulate(resultado, headers=colunas, tablefmt="grid")
        print(tabela)
    else:
        print("Nenhuma tarefa encontrada!")
    
    input("Aperte ENTER para voltar...")
    menu()

# Listar tarefas vencidas
def listar_vencidas():
    os.system("cls")
    print("========== LISTAR TAREFAS VENCIDAS ==========")
    hoje = datetime.now().strftime("%Y-%m-%d")
    
    objTarefa = Tarefa()
    resultado = objTarefa.consultar_vencidas(hoje)
    
    if resultado:
        colunas = ["ID", "Título", "Descrição", "Categoria", "Status", "Prazo", "Nota"]
        tabela = tabulate(resultado, headers=colunas, tablefmt="grid")
        print(tabela)
    else:
        print("Nenhuma tarefa vencida encontrada!")
    
    input("Aperte ENTER para voltar...")
    menu()


# Iniciar o programa
if __name__ == "__main__":
    menu()
