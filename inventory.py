# inventory.py - operações básicas do inventário
# inventario = {id: [nome, quantidade, preco, importado]}

import algorithms


NOME = 0
QUANTIDADE = 1
PRECO = 2
IMPORTADO = 3

ID_MAXIMO = 99999
QUANTIDADE_MAXIMA = 1000000
PRECO_MAXIMO = 10000000.0

inventario = {}

# def validar_nome

# def adicionar_produto

def adicionar(id_produto, nome, quantidade, preco, importado):
    if id_produto in inventario:
        return False
    inventario[id_produto] = [nome, quantidade, preco, importado]
    return True


def remover(id_produto):
    if id_produto not in inventario:
        return False
    del inventario[id_produto]
    return True

# def atualizar

# def buscar por id

def busca_linear(nome):
    # olha produto por produto até achar
    for id_produto in inventario:
        if inventario[id_produto][0].lower() == nome.lower():
            return id_produto
    return None


# def insertion_sort(lista):
#     # ordena a lista de registros [id, nome, qtd, preco, importado] pelo nome
#     for i in range(1, len(lista)):
#         atual = lista[i]
#         j = i - 1
#         while j >= 0 and lista[j][1].lower() > atual[1].lower():
#             lista[j + 1] = lista[j]
#             j -= 1
#         lista[j + 1] = atual
#     return lista


def listar_ordenado():
    lista = []
    for id_produto in inventario:
        lista.append([id_produto] + inventario[id_produto])
    if len(lista) <= 100:
        return algorithms.insertion_sort(lista)
    else: 
        return algorithms.merge_sort(lista)

# calcular_estatiticas
