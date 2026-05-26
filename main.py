# main.py
from src.repository.sqlite_repo import SqliteRepository
from src.services.auth_service import AuthService
from src.services.finance_service import FinanceService
# Importamos a classe que realmente gerencia o Login e Cadastro
from src.views.login_cadastro import LoginCadastro 

def main():
    repo = SqliteRepository()
    auth_service = AuthService(repo)
    finance_service = FinanceService(repo)

    # Inicializamos o app direto pela tela de login
    app = LoginCadastro(auth_service, finance_service)
    
    # Agora a função vai existir!
    app.tela_login()
    app.iniciar()

if __name__ == "__main__":
    main()