from datetime import datetime

class transacao:
    """Representa uma transação financeira de entrada ou saída."""
    def __init__(self, tipo: str, valor: float, descricao: str = "S/D", data: str = None):
        self.tipo = tipo.upper()
        self.valor = valor(float)
        self.descricao = descricao
        self.data = data if data else datetime.now().strftime("%d/%m/%y")

    def para_dicionario(self) -> dict:
        return{
            "tipo": self.tipo,
            "valor": self.valor,
            "descricao": self.descricao,
            "data": self.data
        }
    @classmethod
    def do_dicionario(cls, dados: dict):
        return cls(
        tipo = dados.get("tipo", "ENTRADA"),
        valor = dados.get("valor", 0.0),
        descricao = dados.get("descricao", "S/D"),
        data = dados.get("data")
        )