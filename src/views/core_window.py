# src/views/core_window.py
"""
Módulo principal de interface da aplicação.
Contém a classe base (CoreWindow) da qual todas as outras janelas herdam.
Gerencia a janela principal, navegação (menu lateral), temas e internacionalização.
"""

import customtkinter as ctk
import threading
from src.utils.tradutor import Tradutor as _
from src.utils.tradutor import Tradutor

class CoreWindow:
    """
    Classe base para as interfaces gráficas.
    Centraliza as configurações de paleta de cores, menu lateral e controle de sessão.
    """
    def __init__(self, auth_service, finance_service, janela=None):
        # Injeção de dependências: recebe os serviços para lidar com regras de negócio e banco de dados
        self.auth_service = auth_service
        self.finance_service = finance_service
        self.usuario_atual = None # Armazena o usuário logado na sessão atual
        
        # Paleta de Cores Premium (Suporte nativo para Modo Claro e Modo Escuro)
        # O primeiro valor da tupla é a cor no modo claro, o segundo é no modo escuro.
        self.APP_BG = ("#F8FAFC", "#0B0F19")       # Fundo principal da aplicação
        self.CARD_BG = ("#FFFFFF", "#111827")      # Fundo de cartões e formulários
        self.PRIMARY = ("#1E3A8A", "#6366F1")      # Cor primária (Botões, destaques)
        self.ACCENT_GOLD = ("#9A3412", "#F59E0B")  # Cor de acento (Avisos, alertas)
        self.TEXT_MAIN = ("#0F172A", "#F1F5F9")    # Cor principal do texto
        self.TEXT_MUTED = ("#64748B", "#94A3B8")   # Cor de texto secundário (desbotado)
        self.COR_PRINCIPAL = self.PRIMARY
        
        # Se nenhuma janela existente for passada, cria a janela principal (Root)
        if janela is None:
            ctk.set_appearance_mode("dark") # Define o tema escuro como padrão
            self.janela = ctk.CTk()
            self.janela.geometry("950x650") # Dimensões iniciais da janela
            self.janela.title("EasyFinance - Gestão de Negócios B2B")
            self.janela.configure(fg_color=self.APP_BG)
        else:
            # Caso contrário, reaproveita a janela passada por parâmetro
            self.janela = janela

        # Dicionário de mapeamento para o menu suspenso de seleção de idioma
        self.mapa_idiomas = {"Português": "pt", "English": "en", "Español": "es", "Français": "fr"}

    def limpar_janela(self):
        """Limpa todos os widgets (elementos gráficos) da janela principal para garantir uma troca de página limpa."""
        for widget in self.janela.winfo_children():
            widget.destroy()

    def sincronizar_usuario(self, outra_view):
        """Transfere a sessão do usuário logado entre as instâncias das telas ao navegar."""
        self.usuario_atual = outra_view.usuario_atual

    def desenhar_menu_lateral(self, aba_ativa):
        """
        Constrói dinamicamente o menu de navegação lateral (Sidebar).
        
        Args:
            aba_ativa (str): O nome traduzido da aba que está atualmente aberta (para destacá-la).
        """
        # Importações locais (dentro da função) para evitar Erro de Importação Circular
        from src.views.painel_financeiro import PainelFinanceiro
        from src.views.aba_investimentos import AbaInvestimentos
        from src.views.modulos_suporte import ModulosSuporte
        from src.views.login_cadastro import LoginCadastro
        
        # Cria o frame da barra lateral
        sidebar = ctk.CTkFrame(self.janela, width=220, corner_radius=0, fg_color=self.CARD_BG)
        sidebar.pack(side="left", fill="y") # Alinha à esquerda e preenche todo o eixo Y
        
        # Logotipo / Título do App
        lbl_menu = ctk.CTkLabel(sidebar, text="EASYFINANCE", font=("Roboto", 20, "bold"), text_color=self.COR_PRINCIPAL)
        lbl_menu.pack(pady=30)
        
        # Pega a referência correta do repositório (banco de dados)
        repositorio_real = getattr(self.finance_service, 'repo', self.finance_service)
        
        # Expressões lambda funcionam como "fábricas" atrasando a instanciação das telas até que sejam clicadas
        f_view = lambda: PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
        m_view = lambda: ModulosSuporte(self.auth_service, self.finance_service, self.janela)
        l_view = lambda: LoginCadastro(self.auth_service, self.finance_service, self.janela)
        i_view = lambda: AbaInvestimentos(self.janela, repositorio_real, self.usuario_atual)
        
        def alternar_tela(fabrica_view, metodo_tela, nome_da_aba, muda_layout=True, eh_frame_investimentos=False):
            """Função interna que orquestra a destruição da tela atual e renderização da nova."""
            self.limpar_janela() # Limpa a tela
            
            # Se for uma tela interna do sistema, redesenha o menu lateral
            if muda_layout:
                self.desenhar_menu_lateral(nome_da_aba)
                
            # Tratamento especial para a aba de investimentos (que possui uma arquitetura diferente em seu container)
            if eh_frame_investimentos:
                container_painel = fabrica_view()
                container_painel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
                # Inicia a atualização de dados da API de investimentos em uma thread separada para não travar a UI
                if hasattr(container_painel, 'atualizar_painel'):
                    threading.Thread(target=container_painel.atualizar_painel, daemon=True).start()
            else:
                # Instancia a nova tela padrão, passa a sessão de usuário e o banco de dados
                instancia = fabrica_view()
                instancia.usuario_atual = self.usuario_atual
                instancia.repository = repositorio_real
                # Fallback de segurança caso a tela não tenha o método de alertas
                if not hasattr(instancia, 'renderizar_alertas_dashboard'):
                    instancia.renderizar_alertas_dashboard = lambda *args, **kwargs: None
                # Executa o método responsável por desenhar o conteúdo específico daquela tela
                metodo_tela(instancia)

        # Definição das rotas do menu: (Texto Traduzido, Fábrica, Método de Renderização, É aba de investimento?)
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
        
        # Loop para gerar dinamicamente os botões do menu lateral
        for nome, fabrica, metodo, eh_invest in abas:
            # Destaca o botão atual com a cor primária, os demais ficam transparentes
            cor_botao = self.COR_PRINCIPAL if nome == aba_ativa else "transparent"
            
            # Função geradora de escopo para prender corretamente as variáveis do loop ao botão
            def criar_comando(f=fabrica, m=metodo, n=nome, inv=eh_invest):
                return lambda: alternar_tela(f, m, nome_da_aba=n, muda_layout=True, eh_frame_investimentos=inv)
                
            btn = ctk.CTkButton(sidebar, text=nome, fg_color=cor_botao, anchor="w", command=criar_comando())
            btn.pack(fill="x", padx=10, pady=5)
            
        # Botão de Logout fixado na parte inferior
        btn_sair = ctk.CTkButton(
            sidebar, text=_.t("btn_sair"), fg_color="#c0392b", hover_color="#962d22",
            command=lambda: alternar_tela(l_view, LoginCadastro.tela_login, nome_da_aba="Login", muda_layout=False, eh_frame_investimentos=False)
        )
        btn_sair.pack(side="bottom", fill="x", padx=10, pady=(10, 20))

        # Seletor de Idioma em tempo real
        self.combo_idioma = ctk.CTkComboBox(
            sidebar, 
            values=list(self.mapa_idiomas.keys()), 
            command=lambda v: self.mudar_idioma_sistema(v, aba_ativa),
            width=160
        )
        # Define o texto do combo box para refletir o idioma atual corretamente
        idioma_invertido = {v: k for k, v in self.mapa_idiomas.items()}
        self.combo_idioma.set(idioma_invertido.get(Tradutor.IDIOMA_ATUAL, "Português"))
        self.combo_idioma.pack(side="bottom", pady=5, padx=10)

    def mudar_idioma_sistema(self, idioma_escolhido, aba_ativa_atual):
        """
        Altera o idioma global da aplicação e recarrega a tela ativa no novo idioma.
        """
        from src.views.painel_financeiro import PainelFinanceiro
        from src.views.modulos_suporte import ModulosSuporte
        from src.views.aba_investimentos import AbaInvestimentos
        from src.utils.tradutor import Tradutor
        import threading

        # 1. Troca o idioma na classe estática do tradutor
        sigla = self.mapa_idiomas.get(idioma_escolhido, "pt")
        Tradutor.mudar_idioma(sigla)
        
        # 2. Converte o nome visual da aba no idioma anterior para a chave de dicionário e depois para o novo idioma
        chave_original = self.converter_nome_aba_chave(aba_ativa_atual)
        nova_aba_visual = Tradutor.t(chave_original)

        # 3. Limpa tudo e recria o menu já traduzido
        self.limpar_janela()
        self.desenhar_menu_lateral(nova_aba_visual)

        repositorio_real = getattr(self.finance_service, 'repo', self.finance_service)

        # 4. Árvore de decisão (Switch-case) para renderizar a exata tela em que o usuário estava
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
        """
        Função utilitária (Busca reversa). 
        Recebe um texto que estava aparecendo na interface e descobre qual é a "chave" (ID) 
        dele no dicionário de traduções, permitindo traduzi-lo para o novo idioma.
        """
        for idioma in ["pt", "en", "es", "fr"]:
            for chave, valor in _.t.TEXTOS[idioma].items() if hasattr(_.t, 'TEXTOS') else _.TEXTOS[idioma].items():
                if valor == nome_aba:
                    return chave
        # Retorno seguro (fallback) se a chave não for encontrada
        return "painel_principal"

    def iniciar(self):
        """Inicia o loop principal de eventos do Tkinter, mantendo a janela aberta e interativa."""
        self.janela.mainloop()