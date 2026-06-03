import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from src.utils.tradutor import Tradutor as _

class FormCompraAtivos(ctk.CTkFrame):
    """Componente isolado para o Formulário de Aquisição de Ativos (RF019)."""
    def __init__(self, parent, service, usuario_atual, callback_recarregar_carteira, callback_get_cotacoes):
        super().__init__(parent, corner_radius=12)
        self.service = service
        self.usuario_atual = usuario_atual
        self.recarregar_carteira = callback_recarregar_carteira
        self.get_cotacoes = callback_get_cotacoes
        self.max_permitido = 0.0

        ctk.CTkLabel(self, text=_.t("registro_aquisicao", "Registrar Nova Aquisição"), font=("Arial", 13, "bold")).pack(pady=8)

        ctk.CTkLabel(self, text=_.t("selecione_ativo", "Selecione o Ativo:"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_ticker = ctk.CTkComboBox(self, values=["USD", "EUR"], command=self.vincular_preco_api)
        self.txt_ticker.pack(fill="x", padx=20, pady=(2, 6))

        ctk.CTkLabel(self, text=_.t("preco_unitario", "Preço Unitário do Ativo (R$):"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_preco = ctk.CTkEntry(self, state="disabled", fg_color=("#E2E8F0", "#1E293B"))
        self.txt_preco.pack(fill="x", padx=20, pady=(2, 6))

        self.lbl_limite_maximo = ctk.CTkLabel(self, text=_.t("saldo_calculando", "Saldo disponível: Calculando..."), font=("Arial", 11, "italic"), text_color="#34D399")
        self.lbl_limite_maximo.pack(anchor="w", padx=20, pady=1)

        ctk.CTkLabel(self, text=_.t("qtd_comprar", "Quantidade a Comprar:"), font=("Arial", 11), text_color="#aaa").pack(anchor="w", padx=20)
        self.txt_qtd = ctk.CTkEntry(self, placeholder_text=_.t("ex_qtd", "Ex: 50"))
        self.txt_qtd.pack(fill="x", padx=20, pady=(2, 5))

        self.btn_usar_maximo = ctk.CTkButton(self, text=_.t("btn_qtd_max", "Preencher Quantidade Máxima"), font=("Roboto", 11, "bold"), fg_color="#4B5563", hover_color="#374151", command=self.definir_quantidade_maxima)
        self.btn_usar_maximo.pack(fill="x", padx=20, pady=(0, 8))

        self.btn_salvar = ctk.CTkButton(self, text=_.t("btn_confirmar_inv", "Confirmar Investimento"), fg_color=("#1E3A8A", "#6366F1"), hover_color=("#152a66", "#4f46e5"), text_color=("#0F172A", "#F1F5F9"), font=("Roboto", 13, "bold"), command=self.cadastrar_ativo)
        self.btn_salvar.pack(fill="x", padx=20, pady=10)

    def obter_saldo_atual(self):
        transacoes = getattr(self.usuario_atual, 'transacoes', []) or []
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        return total_receitas - total_despesas

    def vincular_preco_api(self, ativo_selecionado):
        cotacoes = self.get_cotacoes()
        if not cotacoes or ativo_selecionado not in cotacoes: return
        preco_real = cotacoes[ativo_selecionado]
        saldo = self.obter_saldo_atual()

        self.txt_preco.configure(state="normal")
        self.txt_preco.delete(0, "end")
        self.txt_preco.insert(0, f"{preco_real:.2f}")
        self.txt_preco.configure(state="disabled")

        self.max_permitido = (saldo / preco_real) if (saldo > 0 and preco_real > 0) else 0.0
        self.lbl_limite_maximo.configure(text=f"{_.t('saldo_txt', 'Saldo:')} R$ {saldo:.2f} | {_.t('max_permitido', 'Máximo permitido:')} {self.max_permitido:.2f} un.", text_color="#34D399" if self.max_permitido > 0 else "#EF4444")

    def definir_quantidade_maxima(self):
        if not self.get_cotacoes(): return messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_aguarde_api", "Aguarde as cotações."))
        self.txt_qtd.delete(0, "end")
        self.txt_qtd.insert(0, f"{self.max_permitido:.2f}")

    def cadastrar_ativo(self):
        ticker = self.txt_ticker.get().strip().upper()
        qtd_str = self.txt_qtd.get().strip()
        cotacoes = self.get_cotacoes()

        if not cotacoes or ticker not in cotacoes: return messagebox.showerror(_.t("erro"), _.t("msg_erro_ativo_api"))
        if not ticker or not qtd_str: return messagebox.showwarning(_.t("aviso"), _.t("msg_preencha_tudo"))

        try:
            quantidade = float(qtd_str)
            preco_api = cotacoes[ticker]
            total_investimento = quantidade * preco_api
            saldo_disponivel = self.obter_saldo_atual()
            
            if quantidade <= 0: return messagebox.showwarning(_.t("aviso"), _.t("msg_qtd_maior_zero"))
            if total_investimento > saldo_disponivel: return messagebox.showerror(_.t("saldo_insuficiente_tit"), _.t("msg_saldo_insuf"))

            if not hasattr(self.usuario_atual, 'investimentos') or self.usuario_atual.investimentos is None: self.usuario_atual.investimentos = []
            self.usuario_atual.investimentos.append({"ticker": ticker, "quantidade": quantidade, "preco_compra": preco_api, "data_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

            if not hasattr(self.usuario_atual, 'transacoes') or self.usuario_atual.transacoes is None: self.usuario_atual.transacoes = []
            self.usuario_atual.transacoes.append({"tipo": "Despesa", "descricao": f"Investimento: {quantidade:.2f} {ticker}", "valor": total_investimento, "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

            self.service.repository.salvar_usuario(self.usuario_atual)
            self.txt_qtd.delete(0, 'end')
            self.vincular_preco_api(ticker)
            self.recarregar_carteira()
            messagebox.showinfo(_.t("sucesso"), _.t("msg_ativo_comprado"))
        except ValueError:
            messagebox.showerror(_.t("erro"), _.t("msg_erro_num_qtd"))