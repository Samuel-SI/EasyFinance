from src.repository.json_repo import JsonRepository
from src.models.usuario import Usuario
from src.models.transacao import transacao
from src.models.meta import Meta
from src.models.lembrete import Lembrete

class FinanceService:
    """Gerencia as regras de negócio das finanças, controle de metas e trilhas de educação."""

    def __init__(self, repository: JsonRepository):
        self.repo = repository

    def adicionar_transacao( self, usuario: Usuario, tipo: str, valor: float, descricao: str) -> bool:
        """Injeta uma nova movimentação financeira no objeto do usuário."""
        if valor <= 0:
            return False
        
        nova_transacao = transacao(tipo=tipo, valor=valor, descricao=descricao)
        usuario.transacoes.append(nova_transacao)

        self.repo.salvar_usuario(usuario)
        return True
    def adicionar_meta(self, usuario: Usuario, objetivo: str, valor_alvo: float) -> bool:
        """Adiciona um novo objetivo financeiro para gamificação."""
        if valor_alvo <= 0:
            return False
        
        nova_meta = Meta(objetivo=objetivo, valor_alvo=valor_alvo)
        usuario.metas.append(nova_meta)

        usuario.atualizar_gamificacao()
        self.repo.salvar_usuario(usuario)
        return True
    
    def adicionar_lembrete(self, usuario: Usuario, conta: str, data_vencimento: str) -> bool:
        """Agenda um aviso de vencimento de fatura ou imposto."""
        novo_lembrete = Lembrete(conta=conta, data_vencimento=data_vencimento)
        usuario.lembretes.append(novo_lembrete)
        self.repo.salvar_usuario(usuario)
        return True
    
    def computar_curso_concluido(self, usuario: Usuario) -> str: 
        """Soma um curso assistido, recalcula pontos e atualiza o nível B2B."""
        usuario.cursos_concluidos += 1
        usuario.atualizar_gamificacao()
        self.repo.salvar_usuario(usuario)
        return f"Parabéns! Nível atual: {usuario.nivel} {usuario.pontos} pontos acumulados)"