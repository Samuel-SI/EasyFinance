import re
from datetime import datetime

class Validator:
    @staticmethod
    def validar_email(email, usuarios):
        # RF001: .com, @, sem espaços, domínios específicos
        padrao = r'^[a-zA-Z0-9_.+-]+@(gmail|ufrpe)\.com$'
        if not re.match(padrao, email):
            return False, "E-mail inválido! Use domínios @ufrpe ou @gmail (.com)."
        if any(u['email'] == email for u in usuarios):
            return False, "Este e-mail já está cadastrado no sistema."
        return True, ""

    @staticmethod
    def validar_senha(senha, confirmacao):
        # RF002: 4-8 caracteres, 1 número, 1 maiúscula
        if not (4 <= len(senha) <= 8):
            return False, "A senha deve ter entre 4 e 8 caracteres."
        if not any(c.isdigit() for c in senha):
            return False, "A senha deve conter pelo menos um número."
        if not any(c.isupper() for c in senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula."
        if senha != confirmacao:
            return False, "A senha e a confirmação não coincidem."
        return True, ""

    @staticmethod
    def validar_cpf_cnpj(doc, usuarios):
        # RF002: Estrutura XX.XXX.XXX/0001-XX
        padrao = r'^\d{2}\.\d{3}\.\d{3}/0001-\d{2}$'
        if not re.match(padrao, doc):
            return False, "Formato inválido! Use o padrão XX.XXX.XXX/0001-XX."
        if any(u['documento'] == doc for u in usuarios):
            return False, "Este CPF/CNPJ já está vinculado a outra conta."
        return True, ""

    @staticmethod
    def validar_data(data_str):
        # RF004: Impedir data futura
        try:
            data_dt = datetime.strptime(data_str, "%d/%m/%Y")
            if data_dt > datetime.now():
                return False, "Erro: Não é permitido registrar movimentações com datas futuras."
            return True, data_dt
        except ValueError:
            return False, "Formato de data inválido. Use DD/MM/AAAA."