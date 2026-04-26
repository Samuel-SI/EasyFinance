# src/validators.py

def realizar_cadastro(emails_cadastrados, cpfs_cadastrados):
    """
    Coordena o processo de cadastro de novos usuários.
    Realiza validações rigorosas de e-mail, senha e documento (CPF/CNPJ).
    Retorna uma tupla contendo (email, senha, documento) após todas as validações passarem.
    """

    # --- VALIDAÇÃO DE E-MAIL ---
    while True:
        print("\n==== TELA DE CADASTRO ====")
        email = input("Digite o seu e-mail (ex: usuário@gmail.com): ")

        # Regra 1: Impede espaços em branco que invalidam o envio de mensagens
        if " " in email:
            print("ERRO: Não coloque espaços em branco no e-mail.")
            continue

        # Regra 2: Verifica a estrutura básica do endereço
        if "@" not in email or ".com" not in email:
            print("ERRO: Seu e-mail precisa ter '@' e '.com' ! ")
            continue

        # Regra 3: Restrição específica de domínio (Regra de negócio do projeto)
        if not "gmail" in email:
            print("ERRO: Seu e-mail precisa apresentar 'gmail' !")
            continue

        # Regra 4: Verifica duplicidade no banco de dados para evitar contas repetidas
        if email in emails_cadastrados:
            print("Esse e-mail já foi cadastrado!")
            continue
        print("E-mail validado!")
        break
    # --- VALIDAÇÃO DE SENHA ---
    while True:
        senha = input("Digite a senha (ex: Senhausuario1234): ")

        # Verificação de comprimento (Segurança da conta)
        if len(senha) < 7 or len(senha) > 16:
            print("ERRO: Sua senha deve ter de 7 até 16 caracteres!")
            continue 
        
        # Flags para validação de complexidade da senha (números e letras maiúsculas)
        ha_numero = False 
        letra_grande = False

        # Varredura na string para verificar requisitos de segurança
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

        # Confirmação para evitar erros de digitação do usuário
        confirmacao = input("Confirme sua senha: ")
        if confirmacao != senha:
            print("ERRO: Senha e Confirmação de Senha não coincidem.")
            continue   
        print("Senha validada!")
        break

    # --- VALIDAÇÃO DE DOCUMENTO (CPF/CNPJ) ---
    while True:
        cpf_cnpj = input("Digite seu CPF/CNPJ: ")

        # Garante que o usuário não digitou letras ou símbolos
        if not cpf_cnpj.isdigit():
            print("ERRO: Digite apenas números.")
            continue

        # Validação por comprimento: CPF (11) ou CNPJ (14)
        if len(cpf_cnpj) != 11 and len(cpf_cnpj) != 14:
            print("ERRO: Quantidade de dígitos incorreta.")
            continue
        if cpf_cnpj in cpfs_cadastrados:
            print("Esse CPF/CNPJ já está cadastrado.")
            continue
        print("CPF/CNPJ validado!")
        break
    
    # Retorna os dados validados para o loop principal
    return email, senha, cpf_cnpj 