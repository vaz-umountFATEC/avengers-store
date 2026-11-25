# main.py - menu de texto
import sys
import inventory
import algorithms
import auth
import storage

# Operações do Inventário
def mostrar_todos():
    produtos = inventory.listar_ordenado()
    if len(produtos) == 0:
        print("Inventário vazio.")
        return
    for p in produtos:
        print(p[0], "-", p[1], "| qtd:", p[2], "| R$", p[3], "| importado:", p[4])

def adicionar():
    id_produto = int(input("ID: "))
    nome = input("Nome: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))
    importado = input("Importado? (s/n): ") == "s"
    if inventory.adicionar(id_produto, nome, quantidade, preco, importado):
        print("Produto adicionado!")
    else:
        print("Esse ID já existe.")

def remover():
    id_produto = int(input("ID para remover: "))
    if inventory.remover(id_produto):
        print("Removido.")
    else:
        print("ID não encontrado.")

# def atualizar(): ***************

def buscar():
    lista = inventory.listar_ordenado()
    nome = input("Nome do produto: ")
    id_produto = algorithms.bb_invList(lista, nome)
    if id_produto is None:
        print("Não encontrado.")
    else:
        print(id_produto, inventory.inventario[id_produto])

# def exibir_estatisticas(): *************

# Login e Autenticação
def ler_campo_obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor != "":
            return valor

def cadastrar_credenciais():
    usuario = ler_campo_obrigatorio("Novo usuario: ")
    senha = ler_campo_obrigatorio("Nova senha: ")
    auth.salvar_credenciais(usuario, senha)
    print("Credenciais salvas com sucesso!\n")

def realizar_login():
    auth.criar_arquivo_se_nao_existir()
    if not auth.existe_login_cadastrado():
        print("Primeiro acesso detectado. Cadastre um usuário e senha iniciais: ")
        cadastrar_credenciais()

    while True:
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        if auth.verificar_login(usuario, senha):
            print("\nAcesso concedido.")
            break
        else:
            print("Usuário ou senha incorretos. Tente novamente.\n")

def alterar_login():
    print('\n--- Alterar Usuário e Senha ---')
    usuario_atual = input("Usuário atual: ").strip()
    senha_atual = input("Senha atual: ").strip()

    if not auth.verificar_login(usuario_atual, senha_atual):
        print("Credenciais atuais incorretas. Alteração cancelada.")
        return

    cadastrar_credenciais()

def exibir_estatisticas():
    stats = inventory.calcular_estatisticas()
    print('▁▂▃▅▆▅▃▂▁Estatísticas do Inventário▁▂▃▅▆▅▃▂▁')
    print("\n--- Estatísticas do Inventário ---")
    print(f"Produtos cadastrados (IDs únicos): {stats['total_produtos']}")
    print(f"Total de itens em estoque (unidades): {stats['total_unidades']}")
    print(f"Valor total do estoque: R$ {stats['valor_total']:.2f}")
    print(f"Produtos importados: {stats['total_importados']} | Nacionais: {stats['total_nacionais']}")
    if stats["mais_caro"] is not None:
        id_caro, nome_caro, preco_caro = stats["mais_caro"]
        print(f"Produto mais caro: {nome_caro} (ID {id_caro}) - R$ {preco_caro:.2f}")

def main():
    print('''
             █████╗ ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███████╗██████╗ ███████╗    ███████╗████████╗ ██████╗ ██████╗ ███████╗
            ██╔══██╗██║   ██║██╔════╝████╗  ██║██╔════╝ ██╔════╝██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝
            ███████║██║   ██║█████╗  ██╔██╗ ██║██║  ███╗█████╗  ██████╔╝███████╗    ███████╗   ██║   ██║   ██║██████╔╝█████╗  
            ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗╚════██║    ╚════██║   ██║   ██║   ██║██╔══██╗██╔══╝  
            ██║  ██║ ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝███████╗██║  ██║███████║    ███████║   ██║   ╚██████╔╝██║  ██║███████╗
            ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
        \n''')
    
    textoLogin = "▁▂▃▅▆▅▃▂▁Login▁▂▃▅▆▅▃▂▁" 
    print(f"{textoLogin:^134}")
    
    primeiro_acesso = realizar_login()
    # inicializar_inventario(primeiro_acesso)

    while True:
        print("\n1-Adicionar  2-Remover  3-Listar  4-Buscar  0-Sair")
        print('''
            x--------------------------------------------------------x
            |   Escolha uma opção:                                   |
            |                                                        |
            |   1- Adicionar      2- Remover       3- Atualizar      |
            |   4- Listar         5- Buscar        6- Estatísticas   |
            |   7- Alterar Login  0- Salvar e Sair                   |
            x--------------------------------------------------------x
            ''')
        opcao = input("Opção: ")
        if opcao == "1":
            adicionar()
        elif opcao == "2":
            remover()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            mostrar_todos()
        elif opcao == "5":
            buscar()
        elif opcao == "6":
            exibir_estatisticas()
        elif opcao == "7":
            alterar_login()
        elif opcao == "0":
            storage.salvar_inventario(inventory.inventario)
            print("Dados criptografados e salvos em inventario.csv.")
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()
