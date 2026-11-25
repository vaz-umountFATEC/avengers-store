# Cifra de Cesar usada para proteger os dados do inventario.

# Este alfabeto tem letras, numeros, acentos e simbolos.
# O ponto e virgula nao entra aqui porque separa as colunas do CSV.
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑáàâãäéèêëíìîïóòôõöúùûüçñ .,-_:!?\'\"()[]{}/|+*=&%$#@<>~^ºª°"
CHAVE = 23


def cifrar(texto, chave=CHAVE):
    # Começamos com um texto vazio para guardar o resultado.
    resultado = ""

    # Analisamos cada caractere do texto.
    for caractere in texto:
        posicao = ALFABETO.find(caractere)

        # Se o caractere estiver no alfabeto, mudamos sua posicao.
        if posicao != -1:
            nova_posicao = (posicao + chave) % len(ALFABETO)
            resultado = resultado + ALFABETO[nova_posicao]
        else:
            # Se nao estiver, mantemos o caractere como esta.
            resultado = resultado + caractere

    return resultado


def decifrar(texto, chave=CHAVE):
    # Para desfazer a cifra, usamos a chave negativa.
    return cifrar(texto, -chave)


def caracteres_fora_do_alfabeto(texto):
    # Guarda os caracteres que nao podem ser cifrados.
    fora = ""

    for caractere in texto:
        if caractere not in ALFABETO and caractere not in fora:
            fora = fora + caractere

    return fora
