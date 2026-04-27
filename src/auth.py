#src/auth.py
def fazer_login(lista_emails, lista_senhas):
    """ realiza a autenticação do usuário e retorna o email do usuário logado ou None se falhar """
    print("\n" + "="*12 + " TELA DE LOGIN " + "="*12)
    if not lista_emails:
        print("⚠️ Nenhum usuário cadastrado.")
        return None
    email_login = input("E-mail: ")
    senha_login = input("Senha: ")
    
    if email_login in lista_emails:
        indice = lista_emails.index(email_login)
        if senha_login == lista_senhas[indice]:
            print(f"✅ Login realizado com sucesso!")
            return email_login
        else: 
            print("❌ Senha incorreta!")
    else:
        print("❌ Usuário não encontrado!")
    return None
