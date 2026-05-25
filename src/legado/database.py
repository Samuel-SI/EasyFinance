#src/database.py

import json
import os

DB_PATH = os.path.join('data', 'database.json')

def inicializar_banco():
    """
    Verifica se o arquivo de banco de dados existe. Se não existir, cria um novo arquivo JSON vazio.
    """
    if not os.path.exists(DB_PATH):
        os.makedirs('data', exist_ok=True)

    if not os.path.exists(DB_PATH):
        estrutura_inicial = {
            "usuarios_cadastrados": {},
            "repositorio_dados": {}
        }  
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(estrutura_inicial, f, indent=4, ensure_ascii=False)

def carregar_todo_o_db():
    """
    Carrega o conteúdo completo do banco de dados JSON e retorna como um dicionário.
    """
    if not os.path.exists(DB_PATH):
        inicializar_banco()
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            conteudo = f.read() .strip()
            if not conteudo:
                return {"usuarios_cadastrados": {}, "repositorio_dados": {}}
            return json.loads(conteudo)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erro ao carregar o banco de dados: {e}")
        return {
            "usuarios_cadastrados": {},"repositorio_dados": {}
        }
    
def salvar_todo_o_db(dados):
    '''grava o dicionário completo do banco de dados de volta no arquivo JSON'''
    try:
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            f.flush()  # Garante que os dados sejam escritos no disco imediatamente 
            os.fsync(f.fileno())  # Sincroniza o arquivo para evitar perda de dados em caso de falha
    except Exception as e:
        print(f"Erro ao salvar o banco de dados: {e}")

def carregar_sessao_usuario(email_logado):
    """
    SEGURANÇA: Esta função filtra o JSON e entrega apenas o que pertence ao email_logado.
    O sistema nunca 'vê' os dados de outros emails aqui.
    """
    db = carregar_todo_o_db()
    repositorio = db.get("repositorio_dados", {})

    dados_user = repositorio.get(email_logado, {})
    metas = dados_user.get("metas", [])
    lembretes = dados_user.get("lembretes", [])
    entradas = dados_user.get("entradas", [])
    saidas = dados_user.get("saidas", [])
       


    return list(metas), list(lembretes), list(entradas), list(saidas)


def salvar_dados_usuario(email_logado, metas=None, lembretes=None, entradas=None, saidas=None):
    """
    Atualiza apenas o 'bloco' do usuário logado dentro do ficheiro global.
    """
    db = carregar_todo_o_db()

    if email_logado not in db["repositorio_dados"]:
        db["repositorio_dados"][email_logado] = {
            "metas": [], "lembretes": [], "entradas": [], "saidas": []
        }
    user_ref = db["repositorio_dados"][email_logado]

    if metas is not None: user_ref["metas"] = list(metas)
    if lembretes is not None: user_ref["lembretes"] = list(lembretes)
    if entradas is not None: user_ref["entradas"] = list(entradas)
    if saidas is not None: user_ref["saidas"] = list(saidas)

    salvar_todo_o_db(db)

def obter_listas_autenticacao():
    """Retorna as listas de emails, senhas e documentos para o login inicial."""
    db = carregar_todo_o_db()
    usuarios = db.get("usuarios_cadastrados", {})

    emails = list(usuarios.keys())
    senhas = [info["senha"] for info in usuarios.values()]
    documentos = [info["documento"] for info in usuarios.values()]

    return emails, senhas, documentos

def cadastrar_novo_usuario(email, senha, documento):
    """Regista o novo usuário no ficheiro único."""
    db = carregar_todo_o_db()
    db["usuarios_cadastrados"][email] = {"senha": senha, "documento": documento}
    db["repositorio_dados"][email] = {"metas": [], "lembretes": [], "entradas": [], "saidas":[]}
    salvar_todo_o_db(db)