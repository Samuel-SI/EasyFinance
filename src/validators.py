# src/validators.py

def realizar_cadastro(emails_cadastrados, cpfs_cadastrados):
    while True:
        print("\n==== TELA DE CADASTRO ====")
        email = input("Digite o seu e-mail (ex: usuário@gmail.com): ")

        if " " in email:
            print("ERRO: Não coloque espaços em branco no e-mail.")
            continue
        if "@" not in email or ".com" not in email:
            print("ERRO: Seu e-mail precisa ter '@' e '.com' ! ")
            continue
        if not "gmail" in email:
            print("ERRO: Seu e-mail precisa apresentar 'gmail' !")
            continue
        if email in emails_cadastrados:
            print("Esse e-mail já foi cadastrado!")
            continue
        print("E-mail validado!")
        break

    while True:
        senha = input("Digite a senha (ex: Senhausuario1234): ")
        if len(senha) < 7 or len(senha) > 16:
            print("ERRO: Sua senha deve ter de 7 até 16 caracteres!")
            continue 

        ha_numero = False 
        letra_grande = False
        for digito in senha:
            if digito.isdigit():
                ha_numero = True
        if not ha_numero:
            print("ERRO: Sua senha deve conter, ao menos, um número!")
            continue 

        for letra in senha: 
            if letra.isupper(): 
                letra_grande = True
        if not letra_grande: 
            print("ERRO: Sua senha deve conter, ao menos, uma letra maiúscula!")
            continue

        confirmacao = input("Confirme sua senha: ")
        if confirmacao != senha:
            print("ERRO: Senha e Confirmação de Senha não coincidem.")
            continue   
        print("Senha validada!")
        break

    while True:
        cpf_cnpj = input("Digite seu CPF/CNPJ: ")
        if not cpf_cnpj.isdigit():
            print("ERRO: Digite apenas números.")
            continue
        if len(cpf_cnpj) != 11 and len(cpf_cnpj) != 14:
            print("ERRO: Quantidade de dígitos incorreta.")
            continue
        if cpf_cnpj in cpfs_cadastrados:
            print("Esse CPF/CNPJ já está cadastrado.")
            continue
        print("CPF/CNPJ validado!")
        break

    return email, senha, cpf_cnpj