# main.py - menu de texto
import sys
import os
import inventory
import algorithms
import auth
import storage

# Validacao de entrada de dados
def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def ler_float(mensagem, minimo, maximo):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

def ler_nome():
    while True:
        nome = input("Nome: ").strip()
        erro = inventory.validar_nome(nome)
        if erro is None:
            return nome
        print(erro)

def ler_importado():
    while True:
        resp = input("Importado? (s/n): ").strip().lower()
        if resp == "s":
            return True
        if resp == "n":
            return False
        print("Digite apenas 's' ou 'n'.")

# Operações do Inventário
def mostrar_todos():
    produtos = inventory.listar_ordenado()
    if len(produtos) == 0:
        print("Inventário vazio.")
        return

    # descobir a maior largura de cada coluna (comparando os valores com o título)
    larg_id = max([len("ID")] + [len(str(p[0])) for p in produtos])
    larg_nome = max([len("Nome")] + [len(p[1]) for p in produtos])
    larg_qtd = max([len("Qtd")] + [len(str(p[2])) for p in produtos])
    larg_preco = max([len("Preço")] + [len(f"R$ {p[3]:.2f}") for p in produtos])
    larg_imp = len("Importado")

    cabecalho = f"{'ID':<{larg_id}} | {'Nome':<{larg_nome}} | {'Qtd':>{larg_qtd}} | {'Preço':>{larg_preco}} | {'Importado':<{larg_imp}}"
    separador = "-" * len(cabecalho)

    print(separador)
    print(cabecalho)
    print(separador)
    for p in produtos:
        preco = f"R$ {p[3]:.2f}"
        imp = "Sim" if p[4] else "Não"
        print(f"{p[0]:<{larg_id}} | {p[1]:<{larg_nome}} | {p[2]:>{larg_qtd}} | {preco:>{larg_preco}} | {imp:<{larg_imp}}")
    print(separador)

def adicionar():
    id_produto = ler_inteiro("ID: ", 1, inventory.ID_MAXIMO)
    if inventory.buscar_id(id_produto) is not None:
        print("Esse ID já existe.")
        return
    nome = ler_nome()
    quantidade = ler_inteiro("Quantidade: ", 0, inventory.QUANTIDADE_MAXIMA)
    preco = ler_float("Preço: ", 0.0, inventory.PRECO_MAXIMO)
    importado = ler_importado()

    inventory.adicionar(id_produto, nome, quantidade, preco, importado)
    print("Produto adicionado!")

def remover():
    id_produto = ler_inteiro("ID para remover: ", 1, inventory.ID_MAXIMO)
    if inventory.remover(id_produto):
        print("Removido.")
    else:
        print("ID não encontrado.")

def atualizar():
    id_produto = ler_inteiro("ID do produto para atualizar: ", 1, inventory.ID_MAXIMO)
    if inventory.buscar_id(id_produto) is None:
        print("ID não encontrado.")
        return
    print("Informe os novos dados:")
    nome = ler_nome()
    quantidade = ler_inteiro("Nova quantidade: ", 0, inventory.QUANTIDADE_MAXIMA)
    preco = ler_float("Novo preço: ", 0.0, inventory.PRECO_MAXIMO)
    importado = ler_importado()

    inventory.atualizar(id_produto, nome, quantidade, preco, importado)
    print("Produto atualizado!")

def buscar():
    tipo = input("1-ID | 2-Nome (Linear) | 3-Nome (Binária): ").strip()

    if tipo == "1":
        id_produto = ler_inteiro("ID: ", 1, inventory.ID_MAXIMO)
    elif tipo in ("2", "3"):
        nome = input("Nome: ").strip()
        id_produto = inventory.busca_linear(nome) if tipo == "2" else algorithms.bb_invList(inventory.listar_ordenado(), nome)
    else:
        print("Opção inválida.")
        return

    dados = inventory.inventario.get(id_produto)
    if dados is None:
        print("Produto não encontrado.")
    else:
        print(f"ID: {id_produto} | Nome: {dados[0]} | Qtd: {dados[1]} | Preço: R$ {dados[2]:.2f} | Importado: {dados[3]}")

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
    primeiro_acesso = not auth.existe_login_cadastrado()
    if not auth.existe_login_cadastrado():
        print("Primeiro acesso detectado. Cadastre um usuário e senha iniciais: ")
        cadastrar_credenciais()

    while True:
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        if auth.verificar_login(usuario, senha):
            print("\nAcesso concedido.")
            return primeiro_acesso
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

def inicializar_inventario(primeiro_acesso):
    if storage.arquivo_existe():
        inventory.inventario, invalidas = storage.carregar_inventario()
        if invalidas:
            print(f"Aviso: linhas ignoradas por erro/corrupção: {invalidas}")
    elif primeiro_acesso:
        storage.criar_arquivo_vazio()
    else:
        print("\nArquivo inventario.csv não encontrado.")
        escolha = input("Digite 1 para criar um novo arquivo vazio ou 2 para sair: ").strip()
        if escolha == "1":
            storage.criar_arquivo_vazio()
        else:
            print("Encerrando. Coloque o arquivo na pasta e reinicie o programa.")
            sys.exit()

def exibir_estatisticas():
    stats = inventory.calcular_estatisticas()

    if stats["mais_caro"] is not None:
        id_caro, nome_caro, preco_caro = stats["mais_caro"]
        mais_caro_txt = f"{nome_caro} (ID {id_caro}) - R$ {preco_caro:.2f}"
    else:
        mais_caro_txt = "Nenhum produto cadastrado"

    linhas = [
        ("Produtos cadastrados", f"{stats['total_produtos']} (IDs únicos)"),
        ("Total de unidades", str(stats["total_unidades"])),
        ("Valor total do estoque", f"R$ {stats['valor_total']:.2f}"),
        ("Importados / Nacionais", f"{stats['total_importados']} / {stats['total_nacionais']}"),
        ("Produto mais caro", mais_caro_txt),
    ]

    larg_rotulo = max(len(r) for r, _ in linhas)
    conteudo = [f"{r.ljust(larg_rotulo, '.')}: {v}" for r, v in linhas]
    larg_total = max(len("ESTATÍSTICAS DO INVENTÁRIO"), max(len(l) for l in conteudo))
    separador = "-" * larg_total

    print(separador)
    print(f"{'ESTATÍSTICAS DO INVENTÁRIO':^{larg_total}}")
    print(separador)
    for linha in conteudo:
        print(linha)
    print(separador)

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
    inicializar_inventario(primeiro_acesso)

    while True:
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
        os.system("cls" if os.name == "nt" else "clear") # clear no terminal -> melhora o visual
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
