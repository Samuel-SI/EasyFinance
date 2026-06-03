import customtkinter as ctk
from src.utils.tradutor import Tradutor as _

class ListaCarteiraAtivos(ctk.CTkScrollableFrame):
    """Componente isolado para listagem renderizada e reativa da carteira (RF020)."""
    def __init__(self, parent, service, usuario_atual):
        super().__init__(parent, fg_color="transparent")
        self.service = service
        self.usuario_atual = usuario_atual

    def renderizar(self, cotacoes_atuais):
        """Limpa e reconstrói os cards de ativos com base na performance em tempo real."""
        for widget in self.winfo_children():
            widget.destroy()

        investimentos = getattr(self.usuario_atual, 'investimentos', []) or []
        if not investimentos:
            ctk.CTkLabel(self, text=_.t("msg_carteira_vazia_label", "Nenhum ativo comprado ainda."), text_color="#777", font=("Arial", 12, "italic")).pack(pady=30)
            return

        for ativo in investimentos:
            perf = self.service.calcular_performance_ativo(ativo, cotacoes_atuais)
            
            # Cromática Reativa (Verde = Lucro, Vermelho = Prejuízo)
            cor_status = "#2ecc71" if perf["lucro_prejuizo"] > 0 else ("#e74c3c" if perf["lucro_prejuizo"] < 0 else "#94A3B8")
            sinal = "+" if perf["lucro_prejuizo"] > 0 else ""

            card_item = ctk.CTkFrame(self, fg_color="#242424", corner_radius=8)
            card_item.pack(fill="x", pady=5, padx=5)

            frame_linha1 = ctk.CTkFrame(card_item, fg_color="transparent")
            frame_linha1.pack(fill="x", padx=12, pady=(8, 2))
            ctk.CTkLabel(frame_linha1, text=f"📌 {ativo['ticker']}", font=("Arial", 13, "bold"), text_color="#F1F5F9").pack(side="left")
            ctk.CTkLabel(frame_linha1, text=f"Qtd: {ativo['quantidade']:.2f}", font=("Arial", 11), text_color="#94A3B8").pack(side="right")

            frame_linha2 = ctk.CTkFrame(card_item, fg_color="transparent")
            frame_linha2.pack(fill="x", padx=12, pady=(2, 8))
            ctk.CTkLabel(frame_linha2, text=f"{_.t('pago', 'Pago:')} R$ {ativo['preco_compra']:.2f}", font=("Arial", 11), text_color="#aaa").pack(side="left")
            
            texto_rendimento = f"{sinal}R$ {perf['lucro_prejuizo']:.2f} ({sinal}{perf['variacao_percentual']:.2f}%)"
            ctk.CTkLabel(frame_linha2, text=texto_rendimento, font=("Arial", 11, "bold"), text_color=cor_status).pack(side="right")