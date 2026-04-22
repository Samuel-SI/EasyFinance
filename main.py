import sys
from database import Database
from validators import Validator
from finance_engine import FinanceEngine
from Courses import CourseManager

class EasyFinance:
    def __init__(self):
        self.dados = Database.carregar()
        self.usuario_logado = None
        self.course_manager = CourseManager()

    def menu_inicial(self):
        while True:
            print("\n--- BEM-VINDO AO EASYFINANCE ---")
            print("1. Cadastrar Novo Usuário")
            print("2. Login")
            print("0. Sair")
            op = input("Escolha uma opção: ")

            if op == "1": self.tela_cadastro()
            elif op == "2": self.tela_login()
            elif op == "0": sys.exit()

    def tela_cadastro(self):
        print("\n--- CADASTRO  ---")
        nome = input("Nome Completo: ")
        email = input("Digite seu e-mail: ")
        val, msg = Validator.validar_email(email, self.dados['usuarios'])
        if not val: print(msg); return

        senha = input("Crie uma senha: ")
        conf = input("Confirme a senha: ")
        val, msg = Validator.validar_senha(senha, conf)
        if not val: print(msg); return

        doc = input("CPF/CNPJ (XX.XXX.XXX/0001-XX): ")
        val, msg = Validator.validar_cpf_cnpj(doc, self.dados['usuarios'])
        if not val: print(msg); return

        self.dados['usuarios'].append({"email": email, "senha": senha, "documento": doc})
        Database.salvar(self.dados)
        print("Conta criada com sucesso!")

    def tela_login(self):
        email = input("E-mail: ")
        senha = input("Senha: ")
        for u in self.dados['usuarios']:
            if u['email'] == email and u['senha'] == senha:
                self.usuario_logado = email
                self.menu_principal()
                return
        print("E-mail ou senha incorretos.")

    def menu_principal(self):
        while self.usuario_logado:
            saldo = FinanceEngine.calcular_saldo(self.usuario_logado, self.dados['transacoes'])
            print(f"\n--- DASHBOARD | Logado: {self.usuario_logado} ---")
            print(f"SALDO ATUAL: R$ {saldo:.2f}")
            print("-" * 30)
            print("1. Registrar Entrada/Saída\n2. Ver Diagnóstico de Saúde\n3. Aba de Cursos\n4. Sair")
            
            op = input("Selecione: ")
            if op == "1": self.registrar_movimento(saldo)
            elif op == "2": print(f"\n{FinanceEngine.gerar_diagnostico(self.usuario_logado, self.dados['transacoes'])}")
            elif op == "3": self.course_manager.exibir_aba()
            elif op == "4":
                if input("Deseja realmente sair? (S/N): ").upper() == "S":
                    self.usuario_logado = None

    def registrar_movimento(self, saldo_atual):
        tipo = "Entrada" if input("1. Entrada ou 2. Saída? ") == "1" else "Saída"
        try:
            valor = float(input("Valor (R$): "))
            if valor <= 0:
                print("O valor deve ser positivo."); return

            if tipo == "Saída" and valor > saldo_atual:
                if input("⚠️ Atenção: Saldo ficará negativo. Continuar? (S/N): ").upper() != "S":
                    return

            val, data = Validator.validar_data(input("Data (DD/MM/AAAA): "))
            if not val: print(data); return

            desc = input("Descrição (Ex: Aluguel, Venda): ")
            self.dados['transacoes'].append({
                "user_email": self.usuario_logado,
                "tipo": tipo,
                "valor": valor,
                "data": data.strftime("%d/%m/%Y"),
                "desc": desc
            })
            Database.salvar(self.dados)
            print("Registro realizado com sucesso!")
        except ValueError:
            print("Erro: Digite um valor numérico válido.")

if __name__ == "__main__":
    EasyFinance().menu_inicial()