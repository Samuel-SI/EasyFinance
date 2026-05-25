from datetime import datetime

class Lembrete:
    def __init__(self, conta: str, data_vencimento: str):
        self.conta = conta
        self.data_vencimento = data_vencimento
    def calcular_dias_restantes(self) -> int:
        hoje = datetime.now
        try:
            data_venc = datetime.strptime(self.data_vencimento, "%d/%m/%Y")
            diferenca = data_venc - hoje
            return diferenca.days + 1
        except ValueError:
            return 999
    def para_dicionario(self) -> dict:
        return{
            "conta": self.conta,
            "data" : self.data_vencimento
        }
    @classmethod
    def do_dicionario(cls, dados: dict):
        return cls(
            conta = dados.get("conta", ""),
            data = dados.get("data", "")
        )