# funções de hashing do usuário e senha

import hashlib
import os


PASTA_DO_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_LOGIN = os.path.join(PASTA_DO_PROGRAMA, "login.txt")


def gerar_hash(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def criar_arquivo_se_nao_existir():
    # Cria o arquivo de login caso ele ainda não exista.
    if not os.path.exists(ARQUIVO_LOGIN):
        with open(ARQUIVO_LOGIN, "w", encoding="utf-8"):
            pass


def ler_credenciais():
    # Lê os hashes salvos no arquivo.
    hash_usuario = ""
    hash_senha = ""

    if not os.path.exists(ARQUIVO_LOGIN):
        return hash_usuario, hash_senha

    with open(ARQUIVO_LOGIN, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if "=" not in linha:
                continue

            campo, valor = linha.split("=", 1)
            campo = campo.strip()
            valor = valor.strip()

            if campo == "login":
                hash_usuario = valor
            elif campo == "senha":
                hash_senha = valor

    return hash_usuario, hash_senha


def existe_login_cadastrado():
    # Confere se já existem usuário e senha registrados.
    hash_usuario, hash_senha = ler_credenciais()
    return hash_usuario != "" and hash_senha != ""


def salvar_credenciais(usuario, senha):
    # Salva os hashes no lugar das informações originais.
    with open(ARQUIVO_LOGIN, "w", encoding="utf-8") as arquivo:
        arquivo.write("login=" + gerar_hash(usuario) + "\n")
        arquivo.write("senha=" + gerar_hash(senha) + "\n")


def verificar_login(usuario, senha):
    # Compara os hashes digitados com os que estão no arquivo.
    hash_usuario, hash_senha = ler_credenciais()

    return (
        gerar_hash(usuario) == hash_usuario
        and gerar_hash(senha) == hash_senha
    )
