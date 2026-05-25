#src/auth.py
import re

from src.utils.validators import validar_email
from src.database import carregar_todo_o_db, salvar_todo_o_db

def fazer_login():
    """ Realiza a autenticação do usuário consultando o banco de dados JSON """
    db = carregar_todo_o_db()
    usuarios = db.get("usuarios_cadastrados", {})

    print("\n" + "="*12 + " TELA DE LOGIN " + "="*12)

    if not usuarios:
        print("⚠️ Nenhum usuário cadastrado no sistema.")
        return None

    email_login = input("E-mail: ").strip()
    senha_login = input("Senha: ")
    
    # Verifica se o email existe nas chaves do dicionário
    if email_login in usuarios:
        # Verifica se a senha bate com a guardada para aquele email
        if senha_login == usuarios[email_login]["senha"]:
            print(f"✅ Login realizado com sucesso!")
            return email_login
        else: 
            print("❌ Senha incorreta!")
    else:
        print("❌ Usuário não encontrado!")
    
    return None

def criar_conta():
    """ Registra um novo usuário no banco de dados JSON """
    db = carregar_todo_o_db()
    
    print("\n" + "="*12 + " CRIAR CONTA " + "="*12)
    novo_email = input("Digite seu melhor e-mail: ").strip()

    # Validação usando a ferramenta da pasta utils
    if not validar_email(novo_email):
        print("❌ E-mail inválido! Use o formato: nome@exemplo.com")
        return

    if novo_email in db["usuarios_cadastrados"]:
        print("❌ Este e-mail já está cadastrado!")
        return

    nova_senha = input("Crie uma senha: ")
    if len(nova_senha) < 4:
        print("❌ A senha deve ter pelo menos 4 caracteres!")
        return

    # Adiciona o novo usuário ao dicionário
    db["usuarios_cadastrados"][novo_email] = {"senha": nova_senha}
    
    # Salva no arquivo JSON
    salvar_todo_o_db(db)
    print(f"✅ Conta criada com sucesso para {novo_email}!")