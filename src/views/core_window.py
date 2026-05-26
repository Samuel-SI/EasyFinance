# src/views/core_window.py
import customtkinter as ctk

class CoreWindow:
    def __init__(self, auth_service, finance_service, janela=None):
        self.auth_service = auth_service
        self.finance_service = finance_service
        self.usuario_atual = None

        # 🎨 Paleta Premium Adaptativa (Claro, Escuro)
        self.APP_BG = ("#F8FAFC", "#0B0F19")        
        self.CARD_BG = ("#FFFFFF", "#111827")       
        self.PRIMARY = ("#1E3A8A", "#6366F1")       
        self.ACCENT_GOLD = ("#9A3412", "#F59E0B")   
        self.TEXT_MAIN = ("#0F172A", "#F1F5F9")     
        self.TEXT_MUTED = ("#64748B", "#94A3B8")    
        self.COR_PRINCIPAL = self.PRIMARY 

        if janela is None:
            ctk.set_appearance_mode("dark")
            self.janela = ctk.CTk()
            self.janela.geometry("950x650")
            self.janela.title("EasyFinance - Gestão de Negócios B2B")
            self.janela.configure(fg_color=self.APP_BG)
        else:
            self.janela = janela

    def limpar_janela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def sincronizar_usuario(self, outra_view):
        """Transfere a sessão do usuário logado entre as instâncias das telas."""
        self.usuario_atual = outra_view.usuario_atual

    def desenhar_menu_lateral(self, aba_ativa):
        from src.views.painel_financeiro import PainelFinanceiro
        from src.views.modulos_suporte import ModulosSuporte
        from src.views.login_cadastro import LoginCadastro

        sidebar = ctk.CTkFrame(self.janela, width=220, corner_radius=0, fg_color=self.CARD_BG)
        sidebar.pack(side="left", fill="y")

        lbl_menu = ctk.CTkLabel(sidebar, text="EASYFINANCE", font=("Roboto", 20, "bold"), text_color=self.COR_PRINCIPAL)
        lbl_menu.pack(pady=30)

        # Lazy loading instanciado via funções anônimas para evitar colisões de importação circular
        f_view = lambda: PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
        m_view = lambda: ModulosSuporte(self.auth_service, self.finance_service, self.janela)
        l_view = lambda: LoginCadastro(self.auth_service, self.finance_service, self.janela)

        def alternar_tela(classe_view, metodo_tela):
            instancia = classe_view()
            instancia.usuario_atual = self.usuario_atual
            metodo_tela(instancia)

        abas = [
            ("Painel Principal", lambda: alternar_tela(f_view, PainelFinanceiro.tela_dashboard)),
            ("Balanço Geral", lambda: alternar_tela(f_view, PainelFinanceiro.tela_balanco)),
            ("Diagnóstico Financeiro", lambda: alternar_tela(f_view, PainelFinanceiro.tela_diagnostico)),
            ("Área de Educação", lambda: alternar_tela(m_view, ModulosSuporte.tela_educacao)),
            ("Metas Financeiras", lambda: alternar_tela(m_view, ModulosSuporte.tela_metas)),
            ("Lembretes de Contas", lambda: alternar_tela(m_view, ModulosSuporte.tela_lembretes)),
            ("Editar Perfil", lambda: alternar_tela(m_view, ModulosSuporte.tela_perfil))
        ]

        for nome, comando in abas:
            cor_botao = self.COR_PRINCIPAL if nome == aba_ativa else "transparent"
            btn = ctk.CTkButton(sidebar, text=nome, fg_color=cor_botao, anchor="w", command=comando)
            btn.pack(fill="x", padx=10, pady=5)

        btn_sair = ctk.CTkButton(sidebar, text="Sair", fg_color="#c0392b", hover_color="#962d22", 
                               command=lambda: alternar_tela(l_view, LoginCadastro.tela_login))
        btn_sair.pack(side="bottom", fill="x", padx=10, pady=20)

    def iniciar(self):
        self.janela.mainloop()