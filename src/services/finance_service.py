from src.repository.json_repo import JsonRepository
from src.models.usuario import Usuario
from src.models.transacao import transacao
from src.models.meta import Meta
from src.models.lembrete import Lembrete

class FinanceService:
    """Gerencia as regras de negócio das finanças, controle de metas e trilhas de educação."""

    def __init__(self, repository: JsonRepository):
        self.repo = repository

    def adicionar_transacao(self, usuario: Usuario, tipo: str, valor: float, descricao: str) -> bool:
        """Injeta uma nova movimentação financeira no objeto do usuário."""
        if valor <= 0:
            return False
        
        # CORREÇÃO AQUI: Criando um dicionário {} em vez de chamar transacao()
        nova_transacao = {"tipo": tipo, "valor": valor, "descricao": descricao}
        
        # Garante que a lista de transações existe antes de adicionar
        if not hasattr(usuario, 'transacoes'):
            usuario.transacoes = []
            
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
    
    def adicionar_meta(self, usuario: Usuario, objetivo: str, valor: float) -> bool:
        """Adiciona uma nova meta financeira no formato de dicionário aceito pelo SQLite."""
        if valor <= 0:
            return False
            
        # Criando o formato dicionário {} exato que o seu sqlite_repo espera ler
        nova_meta = {"objetivo": objetivo, "valor": valor}
        
        if not hasattr(usuario, 'metas'):
            usuario.metas = []
            
        usuario.metas.append(nova_meta)
        
        # Grava a alteração direto no banco SQLite
        self.repo.salvar_usuario(usuario)
        return True
    
    def adicionar_lembrete(self, usuario: Usuario, conta: str, data: str) -> bool:
        """Salva um novo lembrete de conta a pagar no formato correto para o banco de dados."""
        # Criação do dicionário mapeado com as chaves exatas que o seu sqlite_repo espera ler
        novo_lembrete = {"conta": conta, "data": data}
        
        if not hasattr(usuario, 'lembretes'):
            usuario.lembretes = []
            
        usuario.lembretes.append(novo_lembrete)
        
        # Sincroniza a modificação direto com a persistência do SQLite
        self.repo.salvar_usuario(usuario)
        return True
    
    def computar_curso_concluido(self, usuario: Usuario) -> str: 
        """Soma um curso assistido, recalcula pontos e atualiza o nível B2B."""
        usuario.cursos_concluidos += 1
        usuario.atualizar_gamificacao()
        self.repo.salvar_usuario(usuario)
        return f"Parabéns! Nível atual: {usuario.nivel} {usuario.pontos} pontos acumulados)"
    
    def concluir_curso(self, usuario, nome_curso, pontos_do_curso):
        """Adiciona pontos ao usuário apenas após a conclusão de um curso."""
        if not hasattr(usuario, 'cursos_concluidos'):
            usuario.cursos_concluidos = []

        if nome_curso in usuario.cursos_concluidos:
            return False, "Você já concluiu este curso e já recebeu os pontos por ele!"
        
        usuario.pontos += pontos_do_curso
        usuario.cursos_concluidos.append(nome_curso)

        if usuario.pontos >= 100:
            usuario.ranking = "Master (Elite B2B)"
        elif usuario.pontos >= 50:
            usuario.ranking = "Avançado"
        else:
            usuario.ranking = "Iniciante"

        self.repo.salvar_usuario(usuario)

        return True, f"Curso '{nome_curso}' concluido com sucesso! +{pontos_do_curso}pontos técnicos adicionados."
    
    
