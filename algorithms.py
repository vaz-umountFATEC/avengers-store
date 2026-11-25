#!/bin/python3
# algoritmos de busca linear e binária e ordenação

def bb_invList(lista, nome, i=0, f=None):
    """
    busca auruda, binária adaptada pros nomes dentro do dict transformado
    em lista pela função no inventory.py
    """
    if f is None:
        nome=nome.lower()
        f = len(lista)-1
    m = (i+f)//2
    if i>f: return None
    if lista[m][1].lower() == nome: return lista[m][0]
    elif lista[m][1].lower() < nome: return bb_invList(lista, nome, m+1, f)
    else: 
        return bb_invList(lista, nome, i, m-1)

def busca_linear(lista, nome):
    # busca padraozinha
    for p in lista:
        if p[1].upper() == nome.upper():
            return p[0]
    return None

def insertion_sort(lista):
    """ 
    ordena a lista de registros [id, nome, qtd, preco, importado] pelo nome
    """
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and lista[j][1].lower() > atual[1].lower():
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista

    # merge_sort

    # intercalar