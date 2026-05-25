from src.repository.sqlite_repo import SqliteRepository
from src.services.auth_service import AuthService
from src.services.finance_service import FinanceService
from src.views.gui_view import GuiView

def main():
    repo = SqliteRepository()
    auth_service = AuthService(repo)
    finance_service = FinanceService(repo)

    app = GuiView(auth_service, finance_service)

    app.iniciar()

if __name__ == "__main__":
    main()