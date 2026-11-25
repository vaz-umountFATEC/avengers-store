# main.py - menu de texto
import inventory
import algorithms

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


def buscar():
    lista = inventory.listar_ordenado()
    nome = input("Nome do produto: ")
    id_produto = algorithms.bb_invList(lista, nome)
    if id_produto is None:
        print("Não encontrado.")
    else:
        print(id_produto, inventory.inventario[id_produto])

def main():
    while True:
        print("\n1-Adicionar  2-Remover  3-Listar  4-Buscar  0-Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            adicionar()
        elif opcao == "2":
            remover()
        elif opcao == "3":
            mostrar_todos()
        elif opcao == "4":
            buscar()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    main()
