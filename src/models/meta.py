class Meta:
    """Representa um objetivo financeiro do usuário."""

    def __init__(self, objetivo: str, valor_alvo: float, concluida: bool = False):
        self.objetivo = objetivo
        self.valor_alvo = float(valor_alvo)
        self.concluida = concluida
    def para_dicionario(self) -> dict:
        return {
            "objetivo": self.objetivo, 
            "valor_alvo": self.valor_alvo,
            "concluida": self.concluida 
        }
    @classmethod
    def do_dicionario(cls, dados: dict):
        return cls(
            objetivo=dados.get("objetivo", " "),
            valor_alvo = dados.get("valor", 0.0),
            concluida = dados.get("concluida", False)
        )
