import json
import os

class Database:
    FILE_PATH = "easyfinance_db.json"

    @staticmethod
    def carregar():
        if not os.path.exists(Database.FILE_PATH):
            return {"usuarios": [], "transacoes": [], "contas": []}
        try:
            with open(Database.FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            # Caso o arquivo esteja corrompido, retorna estrutura limpa (RF008)
            return {"usuarios": [], "transacoes": [], "contas": []}

    @staticmethod
    def salvar(dados):
        try:
            with open(Database.FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro crítico ao salvar dados: {e}")