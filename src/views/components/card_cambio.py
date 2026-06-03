import customtkinter as ctk
from src.utils.tradutor import Tradutor as _

class CardsCambio(ctk.CTkFrame):
    """Componente visual isolado para exibição de cotações de moedas da API."""
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Card Dólar
        self.card_usd = ctk.CTkFrame(self, height=80, fg_color="#2b2b2b", corner_radius=10)
        self.card_usd.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(self.card_usd, text=_.t("lbl_usd", "Dólar (USD)"), font=("Arial", 11, "bold"), text_color="#aaa").pack(pady=(8, 2))
        self.lbl_usd_valor = ctk.CTkLabel(self.card_usd, text=_.t("carregando", "Carregando..."), font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.lbl_usd_valor.pack(pady=(0, 8))

        # Card Euro
        self.card_eur = ctk.CTkFrame(self, height=80, fg_color="#2b2b2b", corner_radius=10)
        self.card_eur.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(self.card_eur, text=_.t("lbl_eur", "Euro (EUR)"), font=("Arial", 11, "bold"), text_color="#aaa").pack(pady=(8, 2))
        self.lbl_eur_valor = ctk.CTkLabel(self.card_eur, text=_.t("carregando"), font=("Arial", 16, "bold"), text_color="#2ecc71")
        self.lbl_eur_valor.pack(pady=(0, 8))

    def atualizar_valores(self, cotacoes):
        """Alimenta a tela com os dados obtidos da API."""
        if cotacoes:
            self.lbl_usd_valor.configure(text= f"R$ {cotacoes['USD']:.2f}", text_color="#2ecc71")
            self.lbl_eur_valor.configure(text=f"R$ {cotacoes['EUR']:.2f}", text_color="#2ecc71")
        else:
            self.lbl_usd_valor.configure(text=_.t("offline", "Offline"), text_color="#e74c3c")
            self.lbl_eur_valor.configure(text=_.t("offline", "Offline"), text_color="#e74c3c")