# src/validators.py
import re
from datetime import datetime
def validar_email(email):
    regex_email = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if re.match(regex_email, email.lower()):
        return True
    else:
        return False 
    
def validar_senha(senha):
    regex_senha = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&./#])[A-Za-z\d@$!%*?&./#]{7,16}$'
    if re.match(regex_senha, senha):
        return True
    else:
        return False

def validar_cpf_cnpj(documento):
    regex_cpf = r'^\d{11}$'
    regex_cnpj = r'^\d{14}$'
    if re.match(regex_cpf, documento):
        return True
    elif re.match(regex_cnpj, documento):
        return True
    else:
        return False


def realizar_cadastro(emails_cadastrados, cpfs_cadastrados):
    """
    Coordena o processo de cadastro de novos usuários.
    Realiza validações rigorosas de e-mail, senha e documento (CPF/CNPJ).
    Retorna uma tupla contendo (email, senha, documento) após todas as validações passarem.
    """

    # --- VALIDAÇÃO DE E-MAIL ---
    while True:
        print("\n==== TELA DE CADASTRO ====")
        email = input("Digite o seu e-mail (ex: nome@dominio.com): ") .strip()

        # Regra 1: Impede espaços em branco que invalidam o envio de mensagens
        if not validar_email(email):
            print("⚠️ Formato inválido! Use: nome@dominio.com")
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

        if not validar_senha(senha):
            print("\n ⚠️ A senha não atende aos requisitos de segurança:")
            print("- Deve ter entre 7 e 16 caracteres")
            print("- Pelo menos uma letra maiúscula, um número e um caractere especial")
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
        if not validar_cpf_cnpj(cpf_cnpj):
            print("⚠️ Formato inválido! Digite apenas números (11 para CPF ou 14 para CNPJ).")
            continue
        if cpf_cnpj in cpfs_cadastrados:
            print("Esse CPF/CNPJ já está cadastrado.")
            continue
        print("CPF/CNPJ validado!")
        break
    
    # Retorna os dados validados para o loop principal
    return email, senha, cpf_cnpj 

def validar_data(data_str):
    """Retorna True e o objeto datetime se a data for válida, senão False e None."""
    formatos = ["%D/%m/%Y", "%d/%m/%y"]
    for formato in formatos:
        try:
            data_objeto = datetime.strptime(data_str, formato)
            return True, data_objeto
        except ValueError:
            continue
    return False, None 