# inventory.py - operações básicas do inventário
# inventario = {id: [nome, quantidade, preco, importado]}

import algorithms
import crypto

NOME = 0
QUANTIDADE = 1
PRECO = 2
IMPORTADO = 3

ID_MAXIMO = 99999
QUANTIDADE_MAXIMA = 1000000
PRECO_MAXIMO = 10000000.0

inventario = {}

def validar_nome(nome):
    if nome.strip() == "":
        return "O nome não pode ficar vazio."
    fora = crypto.caracteres_fora_do_alfabeto(nome)
    if fora != "":
        return f"Caracteres não permitidos no nome: {fora}"
    return None

# def adicionar(id_produto, nome, quantidade, preco, importado):
#     if id_produto in inventario:
#         return False
#     inventario[id_produto] = [nome, quantidade, preco, importado]
    # return True

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

def atualizar(id_produto, nome, quantidade, preco, importado):
    if id_produto not in inventario:
        return False
    inventario[id_produto] = [nome, quantidade, preco, importado]
    return True

def buscar_id(id_produto):
    return inventario.get(id_produto)

def busca_linear(nome):
    # olha produto por produto até achar
    for id_produto in inventario:
        if inventario[id_produto][0].lower() == nome.lower():
            return id_produto
    return None

def listar_ordenado():
    lista = []
    for id_produto in inventario:
        lista.append([id_produto] + inventario[id_produto])
    if len(lista) <= 100:
        return algorithms.insertion_sort(lista)
    else: 
        return algorithms.merge_sort(lista)

def calcular_estatisticas():
    total_produtos = len(inventario)
    total_unidades = 0
    valor_total = 0.0
    total_importados = 0
    total_nacionais = 0
    mais_caro = None

    for id_produto, dados in inventario.items():
        nome, qtd, preco, importado = dados
        total_unidades += qtd
        valor_total += qtd * preco

        if importado:
            total_importados += 1
        else:
            total_nacionais += 1

        if mais_caro is None or preco > mais_caro[2]:
            mais_caro = (id_produto, nome, preco)

    return {
        "total_produtos": total_produtos,
        "total_unidades": total_unidades,
        "valor_total": valor_total,
        "total_importados": total_importados,
        "total_nacionais": total_nacionais,
        "mais_caro": mais_caro,
    }