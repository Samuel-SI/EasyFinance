class FinanceEngine:
    @staticmethod
    def calcular_saldo(email, transacoes):
        saldo = 0.0
        for t in transacoes:
            if t['user_email'] == email:
                if t['tipo'] == 'Entrada':
                    saldo += t['valor']
                else:
                    saldo -= t['valor']
        return saldo

    @staticmethod
    def gerar_diagnostico(email, transacoes):
        # RF007: Diagnóstico baseado no histórico
        user_trans = [t for t in transacoes if t['user_email'] == email]
        if len(user_trans) < 2:
            return "Coletando dados para seu diagnóstico... Continue registrando!"

        entradas = sum(t['valor'] for t in user_trans if t['tipo'] == 'Entrada')
        saidas = sum(t['valor'] for t in user_trans if t['tipo'] == 'Saída')
        
        if saidas > entradas:
            return "⚠️ Status: Risco de falência detectado. Suas saídas superam as entradas!"
        elif entradas > (saidas * 1.02):
            return "✅ Status: Caminho certo! Sua operação está saudável."
        else:
            return "⚖️ Status: Operação estabilizada. Hora de buscar novos clientes?"