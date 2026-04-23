class GoalManager:
    def __init__(self):
        self.meta_mensal = 0.0

    def configurar_meta(self):
        try:
            print("\n" + "="*30)
            print("  CONFIGURAR META MENSAL")
            print("="*30)
            valor = float(input("Qual o seu objetivo de faturamento para este mês? R$ "))
            if valor < 0:
                print("A meta deve ser um valor positivo.")
                return
            self.meta_mensal = valor
            print(f"Meta de R$ {valor:.2f} gravada com sucesso!")
        except ValueError:
            print("Erro: Introduza um valor numérico válido.")

    def calcular_progresso(self, total_entradas):
        if self.meta_mensal <= 0:
            return "Nenhuma meta definida. Vá a 'Gestão de Metas' para começar."
        
        percentagem = (total_entradas / self.meta_mensal) * 100
        
        # Feedback visual conforme o progresso
        barra = "█" * int(percentagem // 10) + "░" * (10 - int(percentagem // 10))
        
        print(f"\n--- PROGRESSO DA META ---")
        print(f"Objetivo: R$ {self.meta_mensal:.2f}")
        print(f"Alcançado: R$ {total_entradas:.2f}")
        print(f"[{barra}] {percentagem:.1f}%")
        
        if percentagem >= 100:
            return "🏆 Parabéns! Superou a sua meta mensal!"
        elif percentagem >= 75:
            return "🚀 Quase lá! Mantenha o foco nas vendas."
        else:
            return "📉 Continue a registar e a focar no crescimento."