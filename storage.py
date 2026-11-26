# Funcoes para ler e salvar o arquivo inventario.csv.

import os
import crypto
import inventory

PASTA_DO_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_INVENTARIO = os.path.join(PASTA_DO_PROGRAMA, "inventario.csv")
SEPARADOR = ";"

def arquivo_existe():
    # Verifica se o arquivo ja foi criado.
    return os.path.exists(ARQUIVO_INVENTARIO)

def criar_arquivo_vazio():
    # O modo w cria um arquivo vazio.
    arquivo = open(ARQUIVO_INVENTARIO, "w", encoding="utf-8")
    arquivo.close()

# Função importante
def decifrar_linha(linha):
    # Separa os cinco campos usando ponto e virgula.
    campos = linha.split(SEPARADOR)

    if len(campos) != 5:
        return None

    # Descriptografa cada campo separadamente.
    id_texto = crypto.decifrar(campos[0])
    nome = crypto.decifrar(campos[1])
    quantidade_texto = crypto.decifrar(campos[2])
    preco_texto = crypto.decifrar(campos[3])
    importado_texto = crypto.decifrar(campos[4])

    # Converte os textos para os tipos corretos.
    try:
        id_produto = int(id_texto)
        quantidade = int(quantidade_texto)
        preco = float(preco_texto)
    except ValueError:
        return None

    if importado_texto == "True":
        importado = True
    elif importado_texto == "False":
        importado = False
    else:
        return None

    # Confere se os dados estao dentro dos limites do projeto.
    if id_produto < 1 or id_produto > inventory.ID_MAXIMO:
        return None
    if quantidade < 0 or quantidade > inventory.QUANTIDADE_MAXIMA:
        return None
    if preco < 0 or preco > inventory.PRECO_MAXIMO:
        return None
    if inventory.validar_nome(nome) is not None:
        return None

    return [id_produto, nome, quantidade, preco, importado]

def carregar_inventario():
    # O dicionario vai guardar todos os produtos carregados.
    inventario = {}
    linhas_invalidas = []

    arquivo = open(ARQUIVO_INVENTARIO, "r", encoding="utf-8")
    numero_linha = 0

    for linha in arquivo:
        numero_linha = numero_linha + 1
        linha = linha.rstrip("\n\r")

        if linha == "":
            continue

        produto = decifrar_linha(linha)

        if produto is None:
            linhas_invalidas.append(numero_linha)
        else:
            id_produto = produto[0]
            nome = produto[1]
            quantidade = produto[2]
            preco = produto[3]
            importado = produto[4]

            # A funcao do inventory.py adiciona o produto ao dicionario.
            # foi_adicionado = inventory.adicionar(
            #     inventario, id_produto, nome, quantidade, preco, importado
            # )

            # if foi_adicionado == False:
            #     linhas_invalidas.append(numero_linha)
            if id_produto in inventario:
                linhas_invalidas.append(numero_linha)
            else:
                inventario[id_produto] = [nome, quantidade, preco, importado]

    arquivo.close()
    return inventario, linhas_invalidas


def salvar_inventario(inventario):
    # Primeiro montamos todas as linhas que serao gravadas.
    linhas = []

    for id_produto in inventario:
        dados = inventario[id_produto]

        nome = dados[inventory.NOME]
        quantidade = dados[inventory.QUANTIDADE]
        preco = dados[inventory.PRECO]
        importado = dados[inventory.IMPORTADO]

        # O arquivo guarda tudo como texto, por isso usamos str().
        campos = [
            str(id_produto),
            nome,
            str(quantidade),
            "{:.2f}".format(preco),
            str(importado)
        ]

        # Cada campo e criptografado antes de ser salvo.
        campos_cifrados = []
        for campo in campos:
            campos_cifrados.append(crypto.cifrar(campo))

        linha = SEPARADOR.join(campos_cifrados)
        linhas.append(linha + "\n")

    # O modo w substitui o conteudo antigo pelo inventario atualizado.
    arquivo = open(ARQUIVO_INVENTARIO, "w", encoding="utf-8")

    for linha in linhas:
        arquivo.write(linha)

    arquivo.close()