import customtkinter as ctk
from tkinter import messagebox
import os

from src.services.investment_service import InvestmentService
from src.utils.tradutor import Tradutor as _

# Centralização Absoluta de Subcomponentes
from src.views.components.card_cambio import CardsCambio
from src.views.components.conversor_moedas import ComponenteConversor
from src.views.components.form_compra import FormCompraAtivos
from src.views.components.lista_carteira import ListaCarteiraAtivos

class AbaInvestimentos(ctk.CTkFrame):
    """Orquestrador Central da Interface de Investimentos Corporativos."""
    def __init__(self, parent, repository, usuario_atual):
        super().__init__(parent, fg_color="transparent")
        self.repo = repository
        self.usuario_atual = usuario_atual  
        self.service = InvestmentService(self.repo)
        self.cotacoes_atuais = None  

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ----------------------------------------------------
        # COLUNA ESQUERDA (Monitoramento e Inputs)
        # ----------------------------------------------------
        self.frame_esquerda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_esquerda.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_esquerda, text=_.t("titulo_investimentos", "💹 Investimentos Corporativos"), font=("Arial", 22, "bold")).pack(pady=(0, 10), anchor="w")

        # 1. Cards de Monitoramento de Câmbio (API)
        self.componente_cards = CardsCambio(self.frame_esquerda)
        self.componente_cards.pack(fill="x", pady=(0, 15))

        # 2. Formulário de Aquisição de Ativos
        self.formulario = FormCompraAtivos(
            self.frame_esquerda, self.service, self.usuario_atual,
            callback_recarregar_carteira=self.sinalizar_mudanca_carteira,
            callback_get_cotacoes=lambda: self.cotacoes_atuais
        )
        self.formulario.pack(fill="x", pady=5, padx=2)

        # 3. Conversor de Moedas Comercial
        self.conversor = ComponenteConversor(self.frame_esquerda, lambda: self.cotacoes_atuais)
        self.conversor.pack(fill="x", pady=10, padx=2)

        # ----------------------------------------------------
        # COLUNA DIREITA (Carteira e Análise Patrimonial)
        # ----------------------------------------------------
        self.frame_direita = ctk.CTkFrame(self, corner_radius=12)
        self.frame_direita.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.frame_direita, text=_.t("carteira_ativos", "📊 Sua Carteira de Ativos"), font=("Arial", 16, "bold")).pack(pady=10)

        # 4. Lista Scrollável da Carteira
        self.lista_carteira = ListaCarteiraAtivos(self.frame_direita, self.service, self.usuario_atual)
        self.lista_carteira.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # Botões de Operações Analíticas
        self.btn_rebalancear = ctk.CTkButton(self.frame_direita, text=_.t("btn_rebalancear", "⚖️ Verificar Rebalanceamento"), fg_color=("#F59E0B", "#D97706"), hover_color=("#D97706", "#B45309"), text_color="#F1F5F9", font=("Roboto", 13, "bold"), command=self.calcular_rebalanceamento)
        self.btn_rebalancear.pack(fill="x", padx=15, pady=5)

        self.btn_exportar = ctk.CTkButton(self.frame_direita, text=_.t("btn_exportar_rel", "📥 Exportar Relatório Patrimonial"), fg_color=("#10B981", "#059669"), hover_color=("#059669", "#047857"), text_color="#F1F5F9", font=("Roboto", 13, "bold"), command=self.exportar_relatorio)
        self.btn_exportar.pack(fill="x", padx=15, pady=(5, 15))

        self.atualizar_painel()

    def sinalizar_mudanca_carteira(self):
        """Gatilho acionado pelo formulário após uma compra bem-sucedida."""
        self.lista_carteira.renderizar(self.cotacoes_atuais)

    def atualizar_painel(self):
        """Loop de Polling (30s) para atualização de dados em tempo real."""
        try:
            self.cotacoes_atuais = self.service.obter_cotacao_moedas()
            self.componente_cards.atualizar_valores(self.cotacoes_atuais)
            if self.cotacoes_atuais:
                self.formulario.txt_ticker.configure(values=list(self.cotacoes_atuais.keys()))
                self.formulario.vincular_preco_api(self.formulario.txt_ticker.get())
        except Exception:
            self.componente_cards.lbl_usd_valor.configure(text=_.t("erro_api", "Erro API"), text_color="#e74c3c")

        self.lista_carteira.renderizar(self.cotacoes_atuais)
        self.after(30000, self.atualizar_painel)

    def calcular_rebalanceamento(self):
        """[RF024] Processamento analítico de metas (50/50)."""
        investimentos = getattr(self.usuario_atual, 'investimentos', []) or []
        if not investimentos: return messagebox.showinfo(_.t("rebalanceamento"), _.t("msg_carteira_vazia"))
        if not self.cotacoes_atuais: return messagebox.showerror(_.t("erro"), _.t("msg_erro_rebal_api"))

        valores = {"USD": 0.0, "EUR": 0.0}
        for a in investimentos:
            valores[a["ticker"]] += float(a["quantidade"]) * self.cotacoes_atuais.get(a["ticker"], float(a["preco_compra"]))
        
        total = sum(valores.values())
        if total == 0: return
        p_usd = (valores["USD"] / total) * 100

        if 45.0 <= p_usd <= 55.0:
            messagebox.showinfo(_.t("meta_cumprida_tit"), f"{_.t('msg_meta_cumprida')}\n• USD: {p_usd:.1f}%\n• EUR: {(100-p_usd):.1f}%")
        else:
            sugestao = "USD" if p_usd < 50 else "EUR"
            messagebox.showinfo(_.t("sugestao_rebal_tit"), f"💡 Recomendação: Aporte em {sugestao} (Atual: USD {p_usd:.1f}% / EUR {(100-p_usd):.1f}%)")

    def exportar_relatorio(self):
        """[RF022] Geração e despacho SMTP do relatório."""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        caminho = os.path.join(desktop, "Relatorio_Patrimonial.txt")
        with open(caminho, "w", encoding="utf-8") as f: f.write(f"Relatório de {getattr(self.usuario_atual, 'username', 'User')}\n")
        
        if messagebox.askyesno(_.t("relatorio_gerado_tit"), f"Salvo no Desktop. Enviar para {getattr(self.usuario_atual, 'email')}?"):
            self.btn_exportar.configure(text=_.t("btn_enviando_email"), state="disabled")
            self.update_idletasks()
            self.service.enviar_relatorio_por_email(self.usuario_atual, caminho)
            self.btn_exportar.configure(text=_.t("btn_exportar_rel"), state="normal")
            messagebox.showinfo(_.t("sucesso"), _.t("msg_email_enviado"))