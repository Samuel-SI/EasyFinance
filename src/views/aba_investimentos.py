# src/views/aba_investimentos.py
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from src.services.investment_service import InvestmentService
from src.utils.tradutor import Tradutor as _

class AbaInvestimentos(ctk.CTkFrame):
    def __init__(self, parent, repository, usuario_atual):
        super().__init__(parent, fg_color="transparent")
        self.repo = repository
        self.usuario_atual = usuario_atual  # Mantém o usuário logado na sessão
        self.service = InvestmentService(self.repo)
        self.cotacoes_atuais = None  # Guarda o cache da API em tempo real
        
        # Configuração de layout de colunas (Esquerda: Cadastro e Conversor | Direita: Carteira e Rebalanceamento)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------------------=====
        # COLUNA ESQUERDA: Cotações, Cadastro e Conversor Automatizado
        # ----------------------------------------------------------------=====
        self.frame_esquerda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_esquerda.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.titulo = ctk.CTkLabel(self.frame_esquerda, text=_.t("titulo_investimentos", "💹 Investimentos Corporativos"), font=("Arial", 22, "bold"))
        self.titulo.pack(pady=(0, 10), anchor="w")

        # --- Cards de Cotação (API) ---
        self.frame_cards = ctk.CTkFrame(self.frame_esquerda, fg_color="transparent")
        self.frame_cards.pack(fill="x", pady=(0, 15))

        # Card Dólar
        self.card_usd = ctk.CTkFrame(self.frame_cards, height=80, fg_color="#2b2b2b", corner_radius=10)
        self.card_usd.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(self.card_usd, text=_.t("lbl_usd", "Dólar (USD)"), font=("Arial", 11, "bold"), text_color="#aaa").pack(pady=(8, 2))
        self.lbl_usd_valor = ctk.CTkLabel(self.card_usd, text=_.t("carregando", "Carregando..."), font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.lbl_usd_valor.pack(pady=(0, 8))

        # Card Euro
        self.card_eur = ctk.CTkFrame(self.frame_cards, height=80, fg_color="#2b2b2b", corner_radius=10)
        self.card_eur.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(self.card_eur, text=_.t("lbl_eur", "Euro (EUR)"), font=("Arial", 11, "bold"), text_color="#aaa").pack(pady=(8, 2))
        self.lbl_eur_valor = ctk.CTkLabel(self.card_eur, text=_.t("carregando"), font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.lbl_eur_valor.pack(pady=(0, 8))

        # --- Formulário de Cadastro de Ativos Automatizado (RF019) ---
        self.frame_form = ctk.CTkFrame(self.frame_esquerda, corner_radius=12)
        self.frame_form.pack(fill="x", pady=5, padx=2)
        
        ctk.CTkLabel(self.frame_form, text=_.t("registro_aquisicao", "Registrar Nova Aquisição"), font=("Arial", 13, "bold")).pack(pady=8)

        ctk.CTkLabel(self.frame_form, text=_.t("selecione_ativo", "Selecione o Ativo:"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_ticker = ctk.CTkComboBox(self.frame_form, values=["USD", "EUR"], command=self.vincular_preco_api)
        self.txt_ticker.pack(fill="x", padx=20, pady=(2, 6))

        ctk.CTkLabel(self.frame_form, text=_.t("preco_unitario", "Preço Unitário do Ativo (R$):"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_preco = ctk.CTkEntry(self.frame_form, state="disabled", fg_color=("#E2E8F0", "#1E293B"))
        self.txt_preco.pack(fill="x", padx=20, pady=(2, 6))

        self.lbl_limite_maximo = ctk.CTkLabel(self.frame_form, text=_.t("saldo_calculando", "Saldo disponível: Calculando..."), font=("Arial", 11, "italic"), text_color="#34D399")
        self.lbl_limite_maximo.pack(anchor="w", padx=20, pady=1)

        ctk.CTkLabel(self.frame_form, text=_.t("qtd_comprar", "Quantidade a Comprar:"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_qtd = ctk.CTkEntry(self.frame_form, placeholder_text=_.t("ex_qtd", "Ex: 50"))
        self.txt_qtd.pack(fill="x", padx=20, pady=(2, 5))

        self.btn_usar_maximo = ctk.CTkButton(
            self.frame_form, text=_.t("btn_qtd_max", "Preencher Quantidade Máxima"), font=("Roboto", 11, "bold"),
            fg_color="#4B5563", hover_color="#374151", command=self.definir_quantidade_maxima
        )
        self.btn_usar_maximo.pack(fill="x", padx=20, pady=(0, 8))

        self.btn_salvar = ctk.CTkButton(
            self.frame_form, text=_.t("btn_confirmar_inv", "Confirmar Investimento"), 
            fg_color=("#1E3A8A", "#6366F1"), hover_color=("#152a66", "#4f46e5"),
            text_color=("#0F172A", "#F1F5F9"), font=("Roboto", 13, "bold"), command=self.cadastrar_ativo
        )
        self.btn_salvar.pack(fill="x", padx=20, pady=10)

        # --- NOVO BLOCO RF023: Conversor de Moedas Comercial Automatizado ---
        self.frame_conversor = ctk.CTkFrame(self.frame_esquerda, corner_radius=12)
        self.frame_conversor.pack(fill="x", pady=10, padx=2)
        
        ctk.CTkLabel(self.frame_conversor, text=_.t("conversor_moedas", "💱 Conversor de Moedas Comercial (API)"), font=("Arial", 13, "bold")).pack(pady=5)
        
        frame_inputs_conv = ctk.CTkFrame(self.frame_conversor, fg_color="transparent")
        frame_inputs_conv.pack(fill="x", padx=20, pady=5)
        
        self.txt_valor_brl = ctk.CTkEntry(frame_inputs_conv, placeholder_text=_.t("ph_valor_brl", "Valor em Reais (R$)"), width=140)
        self.txt_valor_brl.pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        self.combo_moeda_conv = ctk.CTkComboBox(frame_inputs_conv, values=["USD", "EUR"], width=90)
        self.combo_moeda_conv.pack(side="right")
        
        self.lbl_resultado_conv = ctk.CTkLabel(self.frame_conversor, text=_.t("resultado_conv", "Resultado: ---"), font=("Arial", 12, "bold"), text_color="#6366F1")
        self.lbl_resultado_conv.pack(pady=5)
        
        self.btn_converter = ctk.CTkButton(
            self.frame_conversor, text=_.t("btn_calcular_conv", "Calcular Conversão"), font=("Roboto", 11, "bold"),
            fg_color="#3B82F6", hover_color="#2563EB", command=self.executar_conversao_moeda
        )
        self.btn_converter.pack(fill="x", padx=20, pady=(0, 10))


        # ----------------------------------------------------------------=====
        # COLUNA DIREITA: Carteira Atual, Rebalanceamento e Relatórios
        # ----------------------------------------------------------------=====
        self.frame_direita = ctk.CTkFrame(self, corner_radius=12)
        self.grid_rowconfigure(0, weight=1)
        self.frame_direita.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_direita, text=_.t("carteira_ativos", "📊 Sua Carteira de Ativos"), font=("Arial", 16, "bold")).pack(pady=10)

        # Container com barra de rolagem para listar as compras
        self.lista_carteira = ctk.CTkScrollableFrame(self.frame_direita, fg_color="transparent")
        self.lista_carteira.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # --- NOVO BLOCO RF024: Rebalanceamento de Carteira (Metas) ---
        self.btn_rebalancear = ctk.CTkButton(
            self.frame_direita, text=_.t("btn_rebalancear", "⚖️ Verificar Rebalanceamento (Metas)"),
            fg_color=("#F59E0B", "#D97706"), hover_color=("#D97706", "#B45309"),
            text_color="#F1F5F9", font=("Roboto", 13, "bold"), command=self.calcular_rebalanceamento
        )
        self.btn_rebalancear.pack(fill="x", padx=15, pady=(5, 5))

        # --- Botão de Exportação de Relatórios (RF021) ---
        self.btn_exportar = ctk.CTkButton(
            self.frame_direita, text=_.t("btn_exportar_rel", "📥 Exportar Relatório Patrimonial"),
            fg_color=("#10B981", "#059669"), hover_color=("#059669", "#047857"),
            text_color="#F1F5F9", font=("Roboto", 13, "bold"), command=self.exportar_relatorio
        )
        self.btn_exportar.pack(fill="x", padx=15, pady=(5, 15))

        # Inicializa as funções de carga de dados
        self.atualizar_painel()

    # ==========================================
    # LÓGICA DE INTEGRAÇÃO FINANCEIRA COM A API
    # ==========================================
    def obter_saldo_atual(self):
        transacoes = getattr(self.usuario_atual, 'transacoes', []) or []
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        return total_receitas - total_despesas

    def vincular_preco_api(self, ativo_selecionado):
        if not self.cotacoes_atuais or ativo_selecionado not in self.cotacoes_atuais:
            return

        preco_real = self.cotacoes_atuais[ativo_selecionado]
        saldo = self.obter_saldo_atual()

        self.txt_preco.configure(state="normal")
        self.txt_preco.delete(0, "end")
        self.txt_preco.insert(0, f"{preco_real:.2f}")
        self.txt_preco.configure(state="disabled")

        if saldo > 0 and preco_real > 0:
            self.max_permitido = saldo / preco_real
        else:
            self.max_permitido = 0.0

        self.lbl_limite_maximo.configure(
            text=f"{_.t('saldo_txt', 'Saldo:')} R$ {saldo:.2f} | {_.t('max_permitido', 'Máximo permitido:')} {self.max_permitido:.2f} un.",
            text_color="#34D399" if self.max_permitido > 0 else "#EF4444"
        )

    def definir_quantidade_maxima(self):
        ativo = self.txt_ticker.get()
        if not self.cotacoes_atuais or ativo not in self.cotacoes_atuais:
            return messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_aguarde_api", "Aguarde o carregamento das cotações da API."))
        
        self.txt_qtd.delete(0, "end")
        self.txt_qtd.insert(0, f"{self.max_permitido:.2f}")

    def atualizar_painel(self):
        try:
            cotacoes = self.service.obter_cotacao_moedas()
            
            if cotacoes:
                self.cotacoes_atuais = cotacoes
                self.lbl_usd_valor.configure(text=f"R$ {cotacoes['USD']:.2f}", text_color="#2ecc71")
                self.lbl_eur_valor.configure(text=f"R$ {cotacoes['EUR']:.2f}", text_color="#2ecc71")
                self.txt_ticker.configure(values=list(cotacoes.keys()))
                self.vincular_preco_api(self.txt_ticker.get())
            else:
                self.lbl_usd_valor.configure(text=_.t("offline", "Offline"), text_color="#e74c3c")
                self.lbl_eur_valor.configure(text=_.t("offline", "Offline"), text_color="#e74c3c")
        except Exception:
            self.lbl_usd_valor.configure(text=_. t("erro_api", "Erro API"), text_color="#e74c3c")

        self.renderizar_carteira()
        self.after(30000, self.atualizar_painel)

    # ==========================================
    # LÓGICA DE NEGÓCIO DO CONVERSOR (RF023)
    # ==========================================
    def executar_conversao_moeda(self):
        """RF023: Realiza a conversão instantânea protegida contra falta de rede"""
        valor_brl_str = self.txt_valor_brl.get().strip()
        moeda_alvo = self.combo_moeda_conv.get()
        
        if not self.cotacoes_atuais:
            self.lbl_resultado_conv.configure(text=_.t("erro_conv_off", "Erro: Conversor indisponível (Offline)"), text_color="#EF4444")
            return
            
        if not valor_brl_str:
            messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_insira_brl", "Insira um valor em Reais para efetuar a conversão."))
            return

        try:
            valor_brl = float(valor_brl_str)
            preco_moeda = self.cotacoes_atuais.get(moeda_alvo, 1.0)
            resultado = valor_brl / preco_moeda
            self.lbl_resultado_conv.configure(text=f"{_.t('resultado_txt', 'Resultado:')} {resultado:.2f} {moeda_alvo}", text_color="#10B981")
        except ValueError:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_num", "Digite apenas caracteres numéricos válidos no conversor."))

    # ==========================================
    # LÓGICA DE REBALANCEAMENTO (RF024)
    # ==========================================
    def calcular_rebalanceamento(self):
        """RF024: Avalia a divisão ideal de risco estabelecida em 50% USD / 50% EUR"""
        investimentos = getattr(self.usuario_atual, 'investimentos', []) or []
        
        if not investimentos:
            messagebox.showinfo(_.t("rebalanceamento", "Rebalanceamento"), _.t("msg_carteira_vazia", "Sua carteira está vazia! Sugestão: Comece aportando igualmente em USD e EUR."))
            return

        if not self.cotacoes_atuais:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_rebal_api", "Não é possível rebalancear sem acesso às cotações de mercado."))
            return

        # Calcula o valor atual consolidado de cada ticker
        patrimonio_total = 0.0
        valores_por_ticker = {"USD": 0.0, "EUR": 0.0}

        for ativo in investimentos:
            ticker = ativo["ticker"]
            qtd = float(ativo["quantidade"])
            preco_mercado = self.cotacoes_atuais.get(ticker, float(ativo["preco_compra"]))
            valor_atual = qtd * preco_mercado
            valores_por_ticker[ticker] = valores_por_ticker.get(ticker, 0.0) + valor_atual
            patrimonio_total += valor_atual

        if patrimonio_total == 0:
            return

        # Definição das metas ideais do gestor (50% para cada uma das moedas comerciais)
        percentual_usd = (valores_por_ticker["USD"] / patrimonio_total) * 100
        percentual_eur = (valores_por_ticker["EUR"] / patrimonio_total) * 100

        # Margem aceitável de desvio (Meta cumprida se estiver entre 45% e 55%)
        if 45.0 <= percentual_usd <= 55.0:
            messagebox.showinfo(
                _.t("meta_cumprida_tit", "⚖️ Meta Cumprida!"),
                f"{_.t('msg_meta_cumprida', 'Sua carteira está perfeitamente balanceada de acordo com as diretrizes!')}\n\n"
                f"{_.t('distribuicao_atual', 'Distribuição Atual:')}\n"
                f"• USD: {percentual_usd:.1f}%\n"
                f"• EUR: {percentual_eur:.1f}%"
            )
        else:
            # Sugere aporte na moeda que estiver abaixo da linha de 50%
            sugestao = "USD" if percentual_usd < percentual_eur else "EUR"
            messagebox.showinfo(
                _.t("sugestao_rebal_tit", "⚖️ Sugestão de Rebalanceamento"),
                f"{_.t('msg_desvio_detect', 'Desvio detectado das diretrizes ideais de alocação de risco (50%/50%).')}\n\n"
                f"{_.t('alocacao_atual', 'Alocação Atual:')}\n"
                f"• USD: {percentual_usd:.1f}%\n"
                f"• EUR: {percentual_eur:.1f}%\n\n"
                f"💡 {_.t('recomendacao_rebal', 'Recomendação: Direcione os próximos aportes para adquirir')} {sugestao}."
            )

    # ==========================================
    # ENTRADA DE ATIVOS E COMPRAS
    # ==========================================
    def cadastrar_ativo(self):
        ticker = self.txt_ticker.get().strip().upper()
        qtd_str = self.txt_qtd.get().strip()

        if not self.cotacoes_atuais or ticker not in self.cotacoes_atuais:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_ativo_api", "Ativo ou cotação da API inválidos."))
            return

        if not ticker or not qtd_str:
            messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_preencha_tudo", "Preencha todos os campos do formulário!"))
            return

        try:
            quantidade = float(qtd_str)
            preco_api = self.cotacoes_atuais[ticker]
            total_investimento = quantidade * preco_api
            saldo_disponivel = self.obter_saldo_atual()
            
            if quantidade <= 0:
                messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_qtd_maior_zero", "A quantidade precisa ser maior que zero!"))
                return

            if total_investimento > saldo_disponivel:
                messagebox.showerror(
                    _.t("saldo_insuficiente_tit", "Saldo Insuficiente"), 
                    f"{_.t('msg_saldo_insuf', 'Você não possui saldo em conta para esta operação!')}\n\n"
                    f"{_.t('custo_total', 'Custo Total:')} R$ {total_investimento:.2f}\n"
                    f"{_.t('saldo_atual', 'Saldo Atual:')} R$ {saldo_disponivel:.2f}"
                )
                return

            novo_ativo = {
                "ticker": ticker,
                "quantidade": quantidade,
                "preco_compra": preco_api,
                "data_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            if not hasattr(self.usuario_atual, 'investimentos') or self.usuario_atual.investimentos is None:
                self.usuario_atual.investimentos = []
            self.usuario_atual.investimentos.append(novo_ativo)

            if not hasattr(self.usuario_atual, 'transacoes') or self.usuario_atual.transacoes is None:
                self.usuario_atual.transacoes = []
            
            self.usuario_atual.transacoes.append({
                "tipo": "Despesa",
                "descricao": f"Investimento: Compra de {quantidade:.2f} unidades de {ticker}",
                "valor": total_investimento,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            self.repo.salvar_usuario(self.usuario_atual)
            self.txt_qtd.delete(0, 'end')

            self.vincular_preco_api(ticker)
            self.renderizar_carteira()
            
            messagebox.showinfo(_.t("sucesso", "Sucesso"), f"{_.t('msg_ativo_comprado', 'Ativo comprado!')} {ticker}\n\n{_.t('valor_debitado', 'Valor debitado da conta:')} R$ {total_investimento:.2f}")
        except ValueError:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_num_qtd", "Digite apenas números válidos no campo de Quantidade!"))

    def renderizar_carteira(self):
        for widget in self.lista_carteira.winfo_children():
            widget.destroy()

        if not hasattr(self.usuario_atual, 'investimentos') or not self.usuario_atual.investimentos:
            lbl_vazio = ctk.CTkLabel(self.lista_carteira, text=_.t("msg_carteira_vazia_label", "Nenhum ativo comprado ainda."), text_color="#777", font=("Arial", 12, "italic"))
            lbl_vazio.pack(pady=30)
            return

        for ativo in self.usuario_atual.investimentos:
            perf = self.service.calcular_performance_ativo(ativo, self.cotacoes_atuais)
            
            if perf["lucro_prejuizo"] > 0:
                cor_status = "#2ecc71"
                sinal = "+"
            elif perf["lucro_prejuizo"] < 0:
                cor_status = "#e74c3c"
                sinal = ""
            else:
                cor_status = "#94A3B8"
                sinal = ""

            card_item = ctk.CTkFrame(self.lista_carteira, fg_color="#242424", corner_radius=8)
            card_item.pack(fill="x", pady=5, padx=5)

            frame_linha1 = ctk.CTkFrame(card_item, fg_color="transparent")
            frame_linha1.pack(fill="x", padx=12, pady=(8, 2))
            
            lbl_ticker = ctk.CTkLabel(frame_linha1, text=f"📌 {ativo['ticker']}", font=("Arial", 13, "bold"), text_color="#F1F5F9")
            lbl_ticker.pack(side="left")
            
            lbl_qtd = ctk.CTkLabel(frame_linha1, text=f"Qtd: {ativo['quantidade']:.2f}", font=("Arial", 11), text_color="#94A3B8")
            lbl_qtd.pack(side="right")

            frame_linha2 = ctk.CTkFrame(card_item, fg_color="transparent")
            frame_linha2.pack(fill="x", padx=12, pady=(2, 8))
            
            texto_pago = f"{_.t('pago', 'Pago:')} R$ {ativo['preco_compra']:.2f} ({_.t('total', 'Total:')} R$ {perf['custo_total']:.2f})"
            lbl_pago = ctk.CTkLabel(frame_linha2, text=texto_pago, font=("Arial", 11), text_color="#aaa")
            lbl_pago.pack(side="left")
            
            texto_rendimento = f"{sinal}R$ {perf['lucro_prejuizo']:.2f} ({sinal}{perf['variacao_percentual']:.2f}%)"
            lbl_rendimento = ctk.CTkLabel(frame_linha2, text=texto_rendimento, font=("Arial", 11, "bold"), text_color=cor_status)
            lbl_rendimento.pack(side="right")

    def exportar_relatorio(self):
        # Fallback de segurança temporário caso queira gerar um TXT direto pela view
        if hasattr(self.service, 'exportar_relatorio_txt'):
            sucesso, caminho_arquivo = self.service.exportar_relatorio_txt(self.usuario_atual, self.cotacoes_atuais)
        else:
            # Simula a criação do arquivo se o método do service não estiver exposto como TXT
            import os
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            caminho_arquivo = os.path.join(desktop, "Relatorio_Patrimonial.txt")
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(f"Relatório do usuário {self.usuario_atual.username if hasattr(self.usuario_atual,'username') else 'Cliente'}\n")
            sucesso = True

        if sucesso:
            enviar_agora = messagebox.askyesno(
                _.t("relatorio_gerado_tit", "Relatório Gerado"), 
                f"{_.t('msg_relatorio_salvo', 'O relatório foi salvo em seu Desktop.')}\n\n{_.t('msg_enviar_email', 'Deseja enviar uma cópia para o e-mail:')} {getattr(self.usuario_atual, 'email', 'seu-email@provedor.com')}?"
            )
            
            if enviar_agora:
                self.btn_exportar.configure(text=_.t("btn_enviando_email", "📨 Enviando E-mail..."), state="disabled")
                self.update_idletasks()
                
                email_ok, msg_email = self.service.enviar_relatorio_por_email(self.usuario_atual, caminho_arquivo)
                self.btn_exportar.configure(text=_.t("btn_exportar_rel", "📥 Exportar Relatório Patrimonial"), state="normal")
                
                if email_ok:
                    messagebox.showinfo(_.t("sucesso", "Sucesso!"), f"{_.t('msg_email_enviado', 'Relatório enviado com sucesso para')} {getattr(self.usuario_atual, 'email', 'seu-mail')}!")
                else:
                    messagebox.showerror(_.t("erro_envio_tit", "Erro de Envio"), f"{_.t('msg_erro_envio', 'O arquivo foi salvo localmente, mas não pôde ser enviado por e-mail:')}\n\n{msg_email}")
            else:
                messagebox.showinfo(_.t("concluido", "Concluído"), f"{_.t('msg_relatorio_disp', 'O relatório está disponível em:')}\n{caminho_arquivo}")
        else:
            messagebox.showwarning(_.t("erro_exportacao_tit", "Erro de Exportação"), caminho_arquivo)