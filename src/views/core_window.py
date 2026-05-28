# src/views/core_window.py
import customtkinter as ctk
import threading  # 🧵 Importado para eliminar o congelamento de 1 segundo

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
        """Limpa todos os widgets da janela principal para garantir uma troca de página limpa."""
        for widget in self.janela.winfo_children():
            widget.destroy()

    def sincronizar_usuario(self, outra_view):
        """Transfere a sessão do usuário logado entre as instâncias das telas."""
        self.usuario_atual = outra_view.usuario_atual

    def desenhar_menu_lateral(self, aba_ativa):
        from src.views.painel_financeiro import PainelFinanceiro
        from src.views.aba_investimentos import AbaInvestimentos
        from src.views.modulos_suporte import ModulosSuporte
        from src.views.login_cadastro import LoginCadastro

        # Montagem do painel de navegação esquerdo
        sidebar = ctk.CTkFrame(self.janela, width=220, corner_radius=0, fg_color=self.CARD_BG)
        sidebar.pack(side="left", fill="y")

        lbl_menu = ctk.CTkLabel(sidebar, text="EASYFINANCE", font=("Roboto", 20, "bold"), text_color=self.COR_PRINCIPAL)
        lbl_menu.pack(pady=30)

        # Determina o repositório de dados ativo
        repositorio_real = getattr(self.finance_service, 'repo', self.finance_service)

        # Configuração das Fábricas de Instanciação
        f_view = lambda: PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
        m_view = lambda: ModulosSuporte(self.auth_service, self.finance_service, self.janela)
        l_view = lambda: LoginCadastro(self.auth_service, self.finance_service, self.janela)
        i_view = lambda: AbaInvestimentos(self.janela, repositorio_real, self.usuario_atual)

        def alternar_tela(fabrica_view, metodo_tela, nome_da_aba, muda_layout=True, eh_frame_investimentos=False):
            """Executa a mudança física de tela de forma assíncrona se necessário."""
            self.limpar_janela()
            
            if muda_layout:
                self.desenhar_menu_lateral(nome_da_aba)

            if eh_frame_investimentos:
                # 🚀 INSTANTÂNEO: Renderiza o esqueleto visual imediatamente
                container_painel = fabrica_view()
                container_painel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
                
                if hasattr(container_painel, 'atualizar_painel'):
                    # 🧵 Cria uma linha de execução separada para a API rodar no fundo sem congelar o app
                    thread_api = threading.Thread(target=container_painel.atualizar_painel, daemon=True)
                    thread_api.start()
            else:
                # Sistema legado funcional padrão
                instancia = fabrica_view()
                instancia.usuario_atual = self.usuario_atual
                instancia.repository = repositorio_real
                
                if not hasattr(instancia, 'renderizar_alertas_dashboard'):
                    instancia.renderizar_alertas_dashboard = lambda *args, **kwargs: None
                
                metodo_tela(instancia)

        # Mapeamento de rotas internas
        abas = [
            ("Painel Principal", f_view, PainelFinanceiro.tela_dashboard, False),
            ("Balanço Geral", f_view, PainelFinanceiro.tela_balanco, False),
            ("Diagnóstico Financeiro", f_view, PainelFinanceiro.tela_diagnostico, False),
            ("Investimentos", i_view, None, True), # Flag True para acionar a otimização de segundo plano
            ("Área de Educação", m_view, ModulosSuporte.tela_educacao, False),
            ("Metas Financeiras", m_view, ModulosSuporte.tela_metas, False),
            ("Lembretes de Contas", m_view, ModulosSuporte.tela_lembretes, False),
            ("Editar Perfil", m_view, ModulosSuporte.tela_perfil, False)
        ]

        # Renderização dos botões
        for nome, fabrica, metodo, eh_invest in abas:
            cor_botao = self.COR_PRINCIPAL if nome == aba_ativa else "transparent"
            
            def criar_comando(f=fabrica, m=metodo, n=nome, inv=eh_invest):
                return lambda: alternar_tela(f, m, nome_da_aba=n, muda_layout=True, eh_frame_investimentos=inv)

            btn = ctk.CTkButton(sidebar, text=nome, fg_color=cor_botao, anchor="w", command=criar_comando())
            btn.pack(fill="x", padx=10, pady=5)

        btn_sair = ctk.CTkButton(
            sidebar, text="Sair", fg_color="#c0392b", hover_color="#962d22", 
            command=lambda: alternar_tela(l_view, LoginCadastro.tela_login, nome_da_aba="Login", muda_layout=False, eh_frame_investimentos=False)
        )
        btn_sair.pack(side="bottom", fill="x", padx=10, pady=20)

    def iniciar(self):
        self.janela.mainloop()