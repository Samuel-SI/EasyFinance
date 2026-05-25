from src.models.transacao import transacao
from src.models.meta import Meta
from src.models.lembrete import Lembrete

class Usuario: 
    """Agrega todos os dados, finanças e progresso do microempreendedor."""
    def __init__(self, email: str, documento: str, senha: str = None):
        self.email = email
        self.documento = documento
        self.senha = senha

        self.transacoes = []
        self.metas = []
        self.lembretes = []

        self.cursos_concluidos = 0
        self.pontos = 0
        self.nivel = "Bronze"
    
    def calcular_saldo(self) -> float:
        total_entradas = sum(t.valor for t in self.transacoes if t.tipo == "ENTRADAS")
        total_saidas = sum(t.valor for t in self.transacoes if t.tipo == "SAÍDA")
        return total_entradas - total_saidas
    def atualizar_gamificacao(self):
        metas_batidas = sum(1 for m in self.metas if m.concluida)
        self.pontos = (metas_batidas * 15) + (self.cursos_concluidos * 30)

        if self.pontos >= 150:
            self.nivel = "Red Diamond"
        elif self.pontos >= 100:
            self.nivel = "Diamond"
        elif self.pontos >= 70:
            self.nivel = "Platinum"
        elif self.pontos >= 40:
            self.nivel = "Gold"
        elif self.pontos >= 20:
            self.nivel = "Silver"
        else:
            self.nivel = "Bronze"

    def serializar_dados(self) -> dict:
        return{
            "transacoes": [t.para_dicionario() for t in self.transacoes],
            "metas": [m.para_dicionario() for m in self.metas],
            "lembretes": [l.para_dicionario() for l in self.lembretes],
            "cursos_concluidos": self.cursos_concluidos,
            "pontos": self.pontos,
            "nivel": self.nivel
        }
    def carregar_dados_do_dicionario(self, dados_repo: dict):
        if "entradas" in dados_repo:
            for v in dados_repo.get("entradas", []):
                self.transacoes.append(transacao("ENTRADA", v, "Migração Antiga"))
            for v in dados_repo.get("saídas", []):
                self.transacoes.append(transacao("SAÍDA", v, "Migração Antiga"))
        else:
            for t in dados_repo.get("Transacoes", []):
                self.transacoes.append(transacao.do_dicionario(t))
        
        self.metas =[Meta.do_dicionario(m) for m in dados_repo.get("metas", [])]
        self.lembrete = [Lembrete.do_dicionario(l) for l in dados_repo.get("lembretes", [])]
        self.cursos_concluidos = dados_repo.get("cursos_concluidos", 0)
        self.pontos = dados_repo.get("pontos", 0)
        self.atualizar_gamificacao()

                
