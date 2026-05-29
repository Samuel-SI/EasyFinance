# src/views/core_window.py
import customtkinter as ctk
import threading
from src.utils.tradutor import Tradutor as _
from src.utils.tradutor import Tradutor

class CoreWindow:
    def __init__(self, auth_service, finance_service, janela=None):
        self.auth_service = auth_service
        self.finance_service = finance_service
        self.usuario_atual = None
        
        # Paleta de Cores Premium (Modo Escuro e Claro)
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

        # Mapa de idiomas para o dropdown
        self.mapa_idiomas = {"Português": "pt", "English": "en", "Español": "es", "Français": "fr"}

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
        
        sidebar = ctk.CTkFrame(self.janela, width=220, corner_radius=0, fg_color=self.CARD_BG)
        sidebar.pack(side="left", fill="y")
        
        lbl_menu = ctk.CTkLabel(sidebar, text="EASYFINANCE", font=("Roboto", 20, "bold"), text_color=self.COR_PRINCIPAL)
        lbl_menu.pack(pady=30)
        
        repositorio_real = getattr(self.finance_service, 'repo', self.finance_service)
        
        f_view = lambda: PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
        m_view = lambda: ModulosSuporte(self.auth_service, self.finance_service, self.janela)
        l_view = lambda: LoginCadastro(self.auth_service, self.finance_service, self.janela)
        i_view = lambda: AbaInvestimentos(self.janela, repositorio_real, self.usuario_atual)
        
        def alternar_tela(fabrica_view, metodo_tela, nome_da_aba, muda_layout=True, eh_frame_investimentos=False):
            self.limpar_janela()
            if muda_layout:
                self.desenhar_menu_lateral(nome_da_aba)
            if eh_frame_investimentos:
                container_painel = fabrica_view()
                container_painel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
                if hasattr(container_painel, 'atualizar_painel'):
                    threading.Thread(target=container_painel.atualizar_painel, daemon=True).start()
            else:
                instancia = fabrica_view()
                instancia.usuario_atual = self.usuario_atual
                instancia.repository = repositorio_real
                if not hasattr(instancia, 'renderizar_alertas_dashboard'):
                    instancia.renderizar_alertas_dashboard = lambda *args, **kwargs: None
                metodo_tela(instancia)

        abas = [
            (_.t("painel_principal"), f_view, PainelFinanceiro.tela_dashboard, False),
            (_.t("balanco_geral"), f_view, PainelFinanceiro.tela_balanco, False),
            (_.t("diag_financeiro"), f_view, PainelFinanceiro.tela_diagnostico, False),
            (_.t("investimentos"), i_view, None, True),
            (_.t("area_educacao"), m_view, ModulosSuporte.tela_educacao, False),
            (_.t("metas_financeiras"), m_view, ModulosSuporte.tela_metas, False),
            (_.t("lembretes_contas"), m_view, ModulosSuporte.tela_lembretes, False),
            (_.t("editar_perfil"), m_view, ModulosSuporte.tela_perfil, False)
        ]
        
        for nome, fabrica, metodo, eh_invest in abas:
            cor_botao = self.COR_PRINCIPAL if nome == aba_ativa else "transparent"
            def criar_comando(f=fabrica, m=metodo, n=nome, inv=eh_invest):
                return lambda: alternar_tela(f, m, nome_da_aba=n, muda_layout=True, eh_frame_investimentos=inv)
            btn = ctk.CTkButton(sidebar, text=nome, fg_color=cor_botao, anchor="w", command=criar_comando())
            btn.pack(fill="x", padx=10, pady=5)
            
        btn_sair = ctk.CTkButton(
            sidebar, text=_.t("btn_sair"), fg_color="#c0392b", hover_color="#962d22",
            command=lambda: alternar_tela(l_view, LoginCadastro.tela_login, nome_da_aba="Login", muda_layout=False, eh_frame_investimentos=False)
        )
        btn_sair.pack(side="bottom", fill="x", padx=10, pady=(10, 20))

        self.combo_idioma = ctk.CTkComboBox(
            sidebar, 
            values=list(self.mapa_idiomas.keys()), 
            command=lambda v: self.mudar_idioma_sistema(v, aba_ativa),
            width=160
        )
        idioma_invertido = {v: k for k, v in self.mapa_idiomas.items()}
        self.combo_idioma.set(idioma_invertido.get(Tradutor.IDIOMA_ATUAL, "Português"))
        self.combo_idioma.pack(side="bottom", pady=5, padx=10)

    def mudar_idioma_sistema(self, idioma_escolhido, aba_ativa_atual):
        from src.views.painel_financeiro import PainelFinanceiro
        from src.views.modulos_suporte import ModulosSuporte
        from src.views.aba_investimentos import AbaInvestimentos
        # Importamos a classe explicitamente para blindar o código contra erros de digitação
        from src.utils.tradutor import Tradutor
        import threading

        # 1. CONSERTADO: Troca o idioma usando a classe correta sem o underline extra
        sigla = self.mapa_idiomas.get(idioma_escolhido, "pt")
        Tradutor.mudar_idioma(sigla)
        
        # 2. CONSERTADO: Traduz o nome da aba ativa usando Tradutor.t
        chave_original = self.converter_nome_aba_chave(aba_ativa_atual)
        nova_aba_visual = Tradutor.t(chave_original)

        # 3. Executa a limpeza e recria o menu lateral (Agora vai rodar!)
        self.limpar_janela()
        self.desenhar_menu_lateral(nova_aba_visual)

        repositorio_real = getattr(self.finance_service, 'repo', self.finance_service)

        # 4. Redesenha a aba ativa no novo idioma correspondente
        if chave_original == "painel_principal":
            inst = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_dashboard()
        elif chave_original == "balanco_geral":
            inst = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_balanco()
        elif chave_original == "diag_financeiro":
            inst = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_diagnostico()
        elif chave_original == "investimentos":
            container = AbaInvestimentos(self.janela, repositorio_real, self.usuario_atual)
            container.pack(side="right", fill="both", expand=True, padx=10, pady=10)
            if hasattr(container, 'atualizar_painel'):
                threading.Thread(target=container.atualizar_painel, daemon=True).start()
        elif chave_original == "area_educacao":
            inst = ModulosSuporte(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_educacao()
        elif chave_original == "metas_financeiras":
            inst = ModulosSuporte(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_metas()
        elif chave_original == "lembretes_contas":
            inst = ModulosSuporte(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_lembretes()
        elif chave_original == "editar_perfil":
            inst = ModulosSuporte(self.auth_service, self.finance_service, self.janela)
            inst.usuario_atual = self.usuario_atual; inst.repository = repositorio_real; inst.tela_perfil()

    def converter_nome_aba_chave(self, nome_aba):
        for idioma in ["pt", "en", "es", "fr"]:
            for chave, valor in _.t.TEXTOS[idioma].items() if hasattr(_.t, 'TEXTOS') else _.TEXTOS[idioma].items():
                if valor == nome_aba:
                    return chave
        return "painel_principal"

    def iniciar(self):
        self.janela.mainloop()