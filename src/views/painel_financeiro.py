# src/views/painel_financeiro.py
import customtkinter as ctk
from tkinter import messagebox
from src.views.core_window import CoreWindow

class PainelFinanceiro(CoreWindow):
    def tela_dashboard(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Painel Principal")

        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Painel Principal", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo_atual = total_receitas - total_despesas

        financas_frame = ctk.CTkFrame(content, fg_color="transparent")
        financas_frame.pack(fill="x", pady=10)

        self.criar_card(financas_frame, "Saldo Atual", f"R$ {saldo_atual:.2f}", "#2ecc71" if saldo_atual >= 0 else "#e74c3c")
        self.criar_card(financas_frame, "Receitas do Mês", f"R$ {total_receitas:.2f}", self.COR_PRINCIPAL)
        self.criar_card(financas_frame, "Despesas do Mês", f"R$ {total_despesas:.2f}", "#e74c3c")

        ctk.CTkLabel(content, text="Seu Desempenho B2B", font=("Roboto", 18, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(20, 10))

        gamifica_frame = ctk.CTkFrame(content, fg_color="transparent")
        gamifica_frame.pack(fill="x", pady=10)

        self.criar_card(gamifica_frame, "Sua Pontuação Técnica", f"{self.usuario_atual.pontos} XP", "#f1c40f")
        self.criar_card(gamifica_frame, "Nível do Perfil", f"{self.usuario_atual.ranking}", "#9b59b6")

    def criar_card(self, parent, titulo, valor, cor_valor):
        card = ctk.CTkFrame(parent, width=220, height=100, fg_color=self.CARD_BG)
        card.pack(side="left", padx=(0, 15))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 14), text_color=self.TEXT_MUTED).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=valor, font=("Roboto", 22, "bold"), text_color=cor_valor).pack()

    def tela_balanco(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Balanço Geral")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Fluxo de Caixa e Transações", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=400, height=400, fg_color=self.CARD_BG)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        if not transacoes:
            ctk.CTkLabel(left_col, text="Nenhuma transação registrada.", text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for t in reversed(transacoes):
                t_frame = ctk.CTkFrame(left_col, fg_color=("#EAEAEA", "#1F2937"))
                t_frame.pack(fill="x", pady=4, padx=5)
                
                desc = t.get('descricao', '') if isinstance(t, dict) else getattr(t, 'descricao', '')
                valor = t.get('valor', 0.0) if isinstance(t, dict) else getattr(t, 'valor', 0.0)
                tipo = t.get('tipo', '') if isinstance(t, dict) else getattr(t, 'tipo', '')
                
                cor = "#2ecc71" if tipo == "Receita" else "#e74c3c"
                sinal = "+" if tipo == "Receita" else "-"
                
                ctk.CTkLabel(t_frame, text=f"{desc}", font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(side="left", padx=15, pady=10)
                ctk.CTkLabel(t_frame, text=f"{sinal} R$ {float(valor):.2f}", text_color=cor, font=("Roboto", 14, "bold")).pack(side="right", padx=15, pady=10)

        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text="Nova Movimentação", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN).pack(pady=15)
        
        self.combo_tipo_transacao = ctk.CTkComboBox(right_col, values=["Receita", "Despesa"], width=180)
        self.combo_tipo_transacao.pack(pady=5)
        
        self.entry_desc_transacao = ctk.CTkEntry(right_col, placeholder_text="Descrição (Ex: Venda)", width=180)
        self.entry_desc_transacao.pack(pady=5)
        
        self.entry_valor_transacao = ctk.CTkEntry(right_col, placeholder_text="Valor (Ex: 1500.00)", width=180)
        self.entry_valor_transacao.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text="Registrar", width=180, command=self.salvar_transacao_gui)
        btn.pack(pady=20)

    def salvar_transacao_gui(self):
        tipo = self.combo_tipo_transacao.get()
        desc = self.entry_desc_transacao.get().strip()
        valor_str = self.entry_valor_transacao.get().strip()
        
        if not desc or not valor_str:
            return messagebox.showwarning("Aviso", "Preencha a descrição e o valor.")
            
        try:
            valor = float(valor_str)
            if hasattr(self.finance_service, 'adicionar_transacao'):
                self.finance_service.adicionar_transacao(self.usuario_atual, tipo, valor, desc)
            else:
                if not hasattr(self.usuario_atual, 'transacoes'):
                    self.usuario_atual.transacoes = []
                self.usuario_atual.transacoes.append({"tipo": tipo, "descricao": desc, "valor": valor})
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            messagebox.showinfo("Sucesso", "Transação registrada!")
            self.tela_balanco()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")

    def tela_diagnostico(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Diagnóstico Financeiro")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Relatório de Saúde Financeira", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo = total_receitas - total_despesas
        
        diag_frame = ctk.CTkFrame(content, corner_radius=10, fg_color=self.CARD_BG)
        diag_frame.pack(fill="both", expand=True, pady=10)
        
        if saldo > 0:
            status = "SAUDÁVEL 🟢"
            msg = "Parabéns! Sua empresa está operando no azul. Suas receitas superam as despesas.\nRecomendação: Considere investir o dinheiro excedente para criar uma reserva de emergência."
            cor = "#2ecc71"
        elif saldo < 0:
            status = "EM ALERTA 🔴"
            msg = "Atenção! Sua empresa está gastando mais do que arrecada.\nRecomendação: Revise a aba de 'Balanço Geral' e corte despesas não essenciais imediatamente."
            cor = "#e74c3c"
        else:
            status = "ESTÁVEL 🟡"
            msg = "Sua empresa não tem lucros nem prejuízos no momento.\nRecomendação: Foque em aumentar as vendas ou criar novas fontes de receita."
            cor = "#f1c40f"
            
        ctk.CTkLabel(diag_frame, text=f"Status Atual: {status}", font=("Roboto", 22, "bold"), text_color=cor).pack(pady=(40, 20))
        ctk.CTkLabel(diag_frame, text=msg, font=("Roboto", 16), text_color=self.TEXT_MAIN, wraplength=500, justify="center").pack(pady=20)