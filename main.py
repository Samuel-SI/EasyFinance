# main.py

# Importação da camada de Persistência de Dados (Repository)
from src.repository.sqlite_repo import SqliteRepository
# Importação da camada de Regras de Negócio (Services)
from src.services.auth_service import AuthService
from src.services.finance_service import FinanceService
# Importação da camada Visual / Interface Gráfica (Views)
from src.views.login_cadastro import LoginCadastro 

def main():
    """
    Função principal que gerencia o ciclo de vida inicial do software,
    garantindo o isolamento de responsabilidades e acoplamento fraco.
    """
    # 1. Inicializa a conexão com o banco de dados relacional SQLite.
    # Se o arquivo 'easyfinance.db' não existir localmente, o repositório o criará de forma automática.
    repo = SqliteRepository()
    # 2. Inicializa os serviços injetando o repositório como dependência.
    # Isso permite que os serviços consultem ou salvem dados sem saber detalhes de como o SQL funciona por baixo.
    auth_service = AuthService(repo)
    finance_service = FinanceService(repo)

    # 3. Inicializa a interface gráfica do usuário (GUI).
    # Injeta os serviços de Autenticação e Finanças necessários para o funcionamento das telas.
    app = LoginCadastro(auth_service, finance_service)
    
    # 4. Configura o estado inicial da aplicação para renderizar o frame/tela de Login.
    app.tela_login()
    # 5. Dispara o loop de eventos principal (Main Loop) do CustomTkinter, 
    # mantendo a janela aberta e escutando as interações e cliques do usuário.
    app.iniciar()
# Salvaguarda padrão do Python para garantir que o script só seja executado
# se for chamado diretamente pelo terminal (python main.py), evitando execuções acidentais caso seja importado.
if __name__ == "__main__":
    main()