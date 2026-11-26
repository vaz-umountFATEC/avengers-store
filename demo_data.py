# gera um inventario.csv de demonstração (já cifrado)

import storage

personagens = [
    "Homem de Ferro", "Capitão América", "Thor", "Hulk", "Viúva Negra",
    "Gavião Arqueiro", "Homem-Aranha", "Pantera Negra", "Doutor Estranho",
    "Feiticeira Escarlate", "Visão", "Homem-Formiga", "Vespa",
    "Falcão", "Soldado Invernal"
]

linhas = [
    "Hot Toys 1/6", "Marvel Legends", "Iron Studios 1/10",
    "SH Figuarts", "Funko Pop", "Mafex", "Edição Deluxe"
]

inventario = {}
id_produto = 1

for personagem in personagens:
    for linha in linhas:
        nome = f"Action Figure {personagem} - {linha}"
        quantidade = (id_produto * 3) % 20 + 1
        preco = round(149.90 + (id_produto * 37.5) % 1400, 2)
        importado = linha != "Iron Studios 1/10"

        inventario[id_produto] = [nome, quantidade, preco, importado]
        id_produto += 1

storage.salvar_inventario(inventario)
print(f"{len(inventario)} produtos da Avengers Store salvos e cifrados em inventario.csv.")