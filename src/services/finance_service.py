from src.repository.json_repo import JsonRepository
from src.models.usuario import Usuario
from src.models.transacao import transacao
from src.models.meta import Meta
from src.models.lembrete import Lembrete

class FinanceService:
    """Gerencia as regras de negócio das finanças, controle de metas e trilhas de educação."""

    def __init__(self, repository):
        self.repo = repository

    def adicionar_transacao(self, usuario: Usuario, tipo: str, valor: float, descricao: str) -> bool:
        """Injeta uma nova movimentação financeira no objeto do usuário."""
        if valor <= 0:
            return False
        
        # Criando um dicionário {} em vez de chamar transacao()
        nova_transacao = {"tipo": tipo, "valor": valor, "descricao": descricao}
        
        # Garante que a lista de transações existe antes de adicionar
        if not hasattr(usuario, 'transacoes'):
            usuario.transacoes = []
            
        usuario.transacoes.append(nova_transacao)

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
        return f"Parabéns! Nível atual: {usuario.nivel} ({usuario.pontos} pontos acumulados)"
    
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

        return True, f"Curso '{nome_curso}' concluído com sucesso! +{pontos_do_curso} pontos técnicos adicionados."

    def verificar_custo_oportunidade(self, usuario: Usuario) -> dict:
        """
        Implementação do RF021 - Alerta de Custo de Oportunidade.
        Calcula o saldo em tempo real baseado nas transações e verifica se há capital ocioso.
        """
        saldo_conta_corrente = 0.0
        
        # Varre o extrato do usuário para descobrir o saldo exato agora
        if hasattr(usuario, 'transacoes') and usuario.transacoes:
            for t in usuario.transacoes:
                tipo = t.get('tipo', '').lower()
                valor = float(t.get('valor', 0))
                
                # Se for entrada de dinheiro, soma. Se for despesa, subtrai.
                if tipo in ['receita', 'entrada', 'deposito']:
                    saldo_conta_corrente += valor
                else:
                    saldo_conta_corrente -= valor
        elif hasattr(usuario, 'saldo_corrente'):
            saldo_conta_corrente = usuario.saldo_corrente
            
        # Define um limite de segurança de caixa livre (ex: R$ 10.000,00)
        LIMITE_PARADO = 10000.0
        
        if saldo_conta_corrente > LIMITE_PARADO:
            excesso = saldo_conta_corrente - LIMITE_PARADO
            
            # Simula perda estimando rendimento em CDI/Selic (aprox 10.5% ao ano -> /12 meses)
            perda_estimada_mes = (excesso * 0.105) / 12
            
            return {
                "disparar_alerta": True,
                "saldo": saldo_conta_corrente,
                "excesso": excesso,
                "perda_mensal_estimada": perda_estimada_mes
            }
            
        return {"disparar_alerta": False}