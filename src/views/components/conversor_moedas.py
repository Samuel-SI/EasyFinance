import customtkinter as ctk
from tkinter import messagebox
from src.utils.tradutor import Tradutor as _

class ComponenteConversor(ctk.CTkFrame):
    """Componente visual e lógico do Conversor Comercial RF023."""
    def __init__(self, parent, callback_cotacoes):
        super().__init__(parent, corner_radius=12)
        self.get_cotacoes = callback_cotacoes # Função para buscar o cache da API da view principal
        
        ctk.CTkLabel(self, text=_.t("conversor_moedas", "💱 Conversor de Moedas Comercial (API)"), font=("Arial", 13, "bold")).pack(pady=5)
        
        frame_inputs = ctk.CTkFrame(self, fg_color="transparent")
        frame_inputs.pack(fill="x", padx=20, pady=5)
        
        self.txt_valor_brl = ctk.CTkEntry(frame_inputs, placeholder_text=_.t("ph_valor_brl", "Valor em Reais (R$)"), width=140)
        self.txt_valor_brl.pack(side="left", padx=(0, 10), expand=True, fill="x")
        
        self.combo_moeda_conv = ctk.CTkComboBox(frame_inputs, values=["USD", "EUR"], width=90)
        self.combo_moeda_conv.pack(side="right")
        
        self.lbl_resultado_conv = ctk.CTkLabel(self, text=_.t("resultado_conv", "Resultado: ---"), font=("Arial", 12, "bold"), text_color="#6366F1")
        self.lbl_resultado_conv.pack(pady=5)
        
        self.btn_converter = ctk.CTkButton(self, text=_.t("btn_calcular_conv", "Calcular Conversão"), font=("Roboto", 11, "bold"), fg_color="#3B82F6", hover_color="#2563EB", command=self.executar_conversao_moeda)
        self.btn_converter.pack(fill="x", padx=20, pady=(0, 10))

    def executar_conversao_moeda(self):
        valor_brl_str = self.txt_valor_brl.get().strip()
        moeda_alvo = self.combo_moeda_conv.get()
        cotacoes = self.get_cotacoes()

        if not cotacoes:
            self.lbl_resultado_conv.configure(text=_.t("erro_conv_off", "Erro: Conversor indisponível (Offline)"), text_color="#EF4444")
            return
            
        if not valor_brl_str:
            messagebox.showwarning(_.t("aviso", "Aviso"), _.t("msg_insira_brl", "Insira um valor em Reais."))
            return

        try:
            valor_brl = float(valor_brl_str)
            preco_moeda = cotacoes.get(moeda_alvo, 1.0)
            resultado = valor_brl / preco_moeda
            self.lbl_resultado_conv.configure(text=f"{_.t('resultado_txt', 'Resultado:')} {resultado:.2f} {moeda_alvo}", text_color="#10B981")
        except ValueError:
            messagebox.showerror(_.t("erro", "Erro"), _.t("msg_erro_num", "Digite apenas números."))