# src/views/painel_financeiro.py
import customtkinter as ctk
from tkinter import messagebox
from src.views.core_window import CoreWindow
from src.views.aba_investimentos import AbaInvestimentos
from src.services.finance_service import FinanceService
from src.utils.tradutor import Tradutor as _

class PainelFinanceiro(CoreWindow):
    def tela_dashboard(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("painel_principal"))

        # Inicializa o serviço financeiro corretamente
        self.finance_service = FinanceService(self.auth_service.repo)

        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        # Renderização do banner do RF021
        self.renderizar_alertas_dashboard(content)

        ctk.CTkLabel(content, text=_.t("painel_principal"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))

        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo_atual = total_receitas - total_despesas

        financas_frame = ctk.CTkFrame(content, fg_color="transparent")
        financas_frame.pack(fill="x", pady=10)

        self.criar_card(financas_frame, _.t("saldo_atual"), f"R$ {saldo_atual:.2f}", "#2ecc71" if saldo_atual >= 0 else "#e74c3c")
        self.criar_card(financas_frame, _.t("receitas_mes"), f"R$ {total_receitas:.2f}", self.COR_PRINCIPAL)
        self.criar_card(financas_frame, _.t("despesas_mes"), f"R$ {total_despesas:.2f}", "#e74c3c")

        # =========================================================================
        # ✨ IMPLEMENTAÇÃO DO REQUISITO RF026: CONTROLE DE TETO DE GASTOS (BUDGETING)
        # =========================================================================
        ctk.CTkLabel(content, text=_.t("controle_teto_gastos", "Controle de Teto de Gastos (Budgeting)"), font=("Roboto", 18, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(20, 10))
        
        budget_scroll = ctk.CTkScrollableFrame(content, height=140, fg_color=self.CARD_BG, corner_radius=10)
        budget_scroll.pack(fill="x", pady=(0, 10))

        # Agrupamento dinâmico das despesas por categoria/descrição para monitoramento
        gastos_por_categoria = {}
        for t in transacoes:
            tipo = t.get('tipo', '') if isinstance(t, dict) else getattr(t, 'tipo', '')
            if tipo == "Despesa":
                desc = t.get('descricao', 'Geral') if isinstance(t, dict) else getattr(t, 'descricao', 'Geral')
                val = float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0))
                gastos_por_categoria[desc] = gastos_por_categoria.get(desc, 0.0) + val

        # Definição de metas orçamentárias (Teto padrão corporativo de R$ 3.000,00 por categoria)
        TETO_PADRAO = 3000.0

        if not gastos_por_categoria:
            ctk.CTkLabel(budget_scroll, text=_.t("nenhum_gasto_monitoramento", "Nenhum gasto registrado para monitoramento de teto."), text_color=self.TEXT_MUTED, font=("Roboto", 13)).pack(pady=40)
        else:
            for categoria, total_gasto in gastos_por_categoria.items():
                percentagem = total_gasto / TETO_PADRAO
                percentagem_limitada = min(percentagem, 1.0) # Trava visual para a barra do CustomTkinter

                # Lógica algorítmica de cores exigida pelo RF026
                if percentagem >= 1.0:
                    cor_status = "#e74c3c"     # Vermelho: Estourou 100%
                    texto_status = _.t("orcamento_estourado", "⚠️ ORÇAMENTO ESTOURADO!")
                elif percentagem >= 0.8:
                    cor_status = "#f1c40f"     # Amarelo: Passou de 80% (Alerta)
                    texto_status = _.t("proximo_limite", "🟡 Próximo ao Limite")
                else:
                    cor_status = "#2ecc71"     # Verde: Operando sob controle seguro
                    texto_status = _.t("dentro_do_teto", "🟢 Dentro do Teto")

                # Criação da linha de progresso na listagem
                item_frame = ctk.CTkFrame(budget_scroll, fg_color="transparent")
                item_frame.pack(fill="x", padx=10, pady=6)

                # Rótulos informativos
                lbl_info = ctk.CTkLabel(
                    item_frame, 
                    text=f"{categoria.upper()} — R$ {total_gasto:.2f} / R$ {TETO_PADRAO:.2f} ({percentagem * 100:.1f}%)",
                    font=("Roboto", 13, "bold"),
                    text_color=self.TEXT_MAIN
                )
                lbl_info.pack(side="left")

                lbl_msg_status = ctk.CTkLabel(item_frame, text=texto_status, font=("Roboto", 12, "italic"), text_color=cor_status)
                lbl_msg_status.pack(side="right", padx=(10, 0))

                # Barra de progresso visual do CustomTkinter injetada com a cor reativa
                bar = ctk.CTkProgressBar(budget_scroll, height=10, progress_color=cor_status, fg_color=("#EAEAEA", "#1F2937"))
                bar.set(percentagem_limitada)
                bar.pack(fill="x", padx=10, pady=(0, 10))

        # =========================================================================

        ctk.CTkLabel(content, text=_.t("desempenho_b2b"), font=("Roboto", 18, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(15, 10))

        gamifica_frame = ctk.CTkFrame(content, fg_color="transparent")
        gamifica_frame.pack(fill="x", pady=5)

        self.criar_card(gamifica_frame, _.t("pontuacao_tecnica"), f"{self.usuario_atual.points if hasattr(self.usuario_atual, 'points') else getattr(self.usuario_atual, 'pontos', 0)} XP", "#f1c40f")
        self.criar_card(gamifica_frame, _.t("nivel_perfil"), f"{self.usuario_atual.ranking}", "#9b59b6")

    def criar_card(self, parent, titulo, valor, cor_valor):
        card = ctk.CTkFrame(parent, width=220, height=100, fg_color=self.CARD_BG)
        card.pack(side="left", padx=(0, 15))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 14), text_color=self.TEXT_MUTED).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=valor, font=("Roboto", 22, "bold"), text_color=cor_valor).pack()

    def renderizar_alertas_dashboard(self, parent_frame):
        """Renderiza o banner de custo de oportunidade no topo do painel principal (RF021)"""
        dados_alerta = self.finance_service.verificar_custo_oportunidade(self.usuario_atual)

        if dados_alerta.get("disparar_alerta", False):
            self.frame_alerta_rf021 = ctk.CTkFrame(parent_frame, fg_color=("#FFFBEB", "#78350F"), corner_radius=8, border_width=1, border_color="#F59E0B")
            self.frame_alerta_rf021.pack(fill="x", pady=(0, 20))

            texto_aviso = (
                f"⚠️ {_.t('alerta_oportunidade_1', 'Alerta de Custo de Oportunidade: Sua empresa possui')} R$ {dados_alerta['saldo']:.2f} {_.t('alerta_oportunidade_2', 'parados em caixa.')} "
                f"{_.t('alerta_oportunidade_3', 'Investir o excesso')} (R$ {dados_alerta['excesso']:.2f}) {_.t('alerta_oportunidade_4', 'evitaria uma perda estimada de')} "
                f"R$ {dados_alerta['perda_mensal_estimada']:.2f}/mês."
            )
            
            lbl_aviso = ctk.CTkLabel(
                self.frame_alerta_rf021, 
                text=texto_aviso, 
                font=("Roboto", 13, "bold"), 
                text_color=("#B45309", "#FEF3C7"),
                wraplength=650,
                justify="left"
            )
            lbl_aviso.pack(side="left", padx=15, pady=10, fill="x", expand=True)

            btn_fechar_alerta = ctk.CTkButton(
                self.frame_alerta_rf021,
                text="✕",
                width=30,
                height=30,
                fg_color="transparent",
                hover_color=("#FDE68A", "#92400E"),
                text_color=("#B45309", "#FEF3C7"),
                command=self.fechar_alerta_oportunidade
            )
            btn_fechar_alerta.pack(side="right", padx=10, pady=10)

    def fechar_alerta_oportunidade(self):
        if hasattr(self, 'frame_alerta_rf021') and self.frame_alerta_rf021.winfo_exists():
            self.frame_alerta_rf021.destroy()

    def tela_balanco(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("balanco_geral"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("fluxo_caixa", "Fluxo de Caixa e Transações"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=400, height=400, fg_color=self.CARD_BG)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        if not transacoes:
            ctk.CTkLabel(left_col, text=_.t("nenhuma_transacao"), text_color=self.TEXT_MUTED).pack(pady=20)
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
        
        ctk.CTkLabel(right_col, text=_.t("nova_movimentacao"), font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN).pack(pady=15)
        
        # Mantenho "Receita" e "Despesa" fixos aqui pois eles conectam com a lógica do backend no banco de dados.
        self.combo_tipo_transacao = ctk.CTkComboBox(right_col, values=["Receita", "Despesa"], width=180)
        self.combo_tipo_transacao.pack(pady=5)
        
        self.entry_desc_transacao = ctk.CTkEntry(right_col, placeholder_text=_.t("desc_exemplo", "Descrição (Ex: Marketing)"), width=180)
        self.entry_desc_transacao.pack(pady=5)
        
        self.entry_valor_transacao = ctk.CTkEntry(right_col, placeholder_text=_.t("valor_exemplo", "Valor (Ex: 1500.00)"), width=180)
        self.entry_valor_transacao.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text=_.t("btn_registrar"), width=180, command=self.salvar_transacao_gui)
        btn.pack(pady=20)

    def salvar_transacao_gui(self):
        tipo = self.combo_tipo_transacao.get()
        desc = self.entry_desc_transacao.get().strip()
        valor_str = self.entry_valor_transacao.get().strip()
        
        if not desc or not valor_str:
            return messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_preencha_dados", "Preencha a descrição e o valor."))
            
        try:
            valor = float(valor_str)
            if not hasattr(self, 'finance_service'):
                self.finance_service = FinanceService(self.auth_service.repo)
                
            self.finance_service.adicionar_transacao(self.usuario_atual, tipo, valor, desc)
            messagebox.showinfo(_.t("sucesso", "Sucesso"), _.t("msg_transacao_ok", "Transação registrada!"))
            self.tela_balanco()
        except ValueError:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_valor", "Insira um valor numérico válido."))

    def tela_diagnostico(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("diag_financeiro"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("saude_relatorio"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo = total_receitas - total_despesas
        
        diag_frame = ctk.CTkFrame(content, corner_radius=10, fg_color=self.CARD_BG)
        diag_frame.pack(fill="both", expand=True, pady=10)
        
        if saldo > 0:
            status = _.t("status_saudavel")
            msg = _.t("msg_saudavel")
            cor = "#2ecc71"
        elif saldo < 0:
            status = _.t("status_alerta")
            msg = _.t("msg_alerta")
            cor = "#e74c3c"
        else:
            status = _.t("status_estavel", "ESTÁVEL 🟡")
            msg = _.t("msg_estavel", "Sua empresa não tem lucros nem prejuízos no momento.\nRecomendação: Foque em aumentar as vendas ou criar novas fontes de receita.")
            cor = "#f1c40f"
            
        ctk.CTkLabel(diag_frame, text=f"{_.t('status_atual')} {status}", font=("Roboto", 22, "bold"), text_color=cor).pack(pady=(40, 20))
        ctk.CTkLabel(diag_frame, text=msg, font=("Roboto", 16), text_color=self.TEXT_MAIN, wraplength=500, justify="center").pack(pady=20)

    def tela_investimentos(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("investimentos"))

        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        aba_investimentos = AbaInvestimentos(
            parent=content,
            repository=self.auth_service.repo,
            usuario_atual=self.usuario_atual
        )
        aba_investimentos.pack(fill="both", expand=True)