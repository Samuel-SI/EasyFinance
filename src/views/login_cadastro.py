# src/views/login_cadastro.py
"""
Módulo responsável por gerenciar a interface gráfica de Login e Cadastro de usuários.
Utiliza a biblioteca customtkinter para criar uma interface moderna e o padrão
de injeção de dependências para se comunicar com as regras de negócio.
"""

import customtkinter as ctk
from src.views.core_window import CoreWindow
from src.views.painel_financeiro import PainelFinanceiro
from src.utils.tradutor import Tradutor as _

class LoginCadastro(CoreWindow):
    """
    Classe que representa a janela de Login e Cadastro do sistema.
    Herda de CoreWindow para reaproveitar lógicas de gerenciamento de janelas principais.
    """

    def __init__(self, auth_service, finance_service, janela=None):
        """
        Inicializa a classe de Login e Cadastro.

        Args:
            auth_service: Serviço responsável pela lógica de autenticação (login, cadastro, 2FA).
            finance_service: Serviço responsável pelas operações financeiras (repassado ao painel principal).
            janela: Instância da janela principal do Tkinter/CustomTkinter.
        """
        # Chama o construtor da classe pai (CoreWindow) passando os serviços e a janela base
        super().__init__(auth_service, finance_service, janela)
        
        # Inicializa as variáveis dos elementos de interface como None para armazenamento seguro
        self.entry_senha = None
        self.check_mostrar_senha = None
        self.entry_email = None
        self.entry_senha_cad = None

    def tela_login(self):
        """
        Constrói e exibe a interface de login na tela.
        Limpa os elementos anteriores da janela e desenha os novos componentes gráficos.
        """
        # Limpa qualquer elemento que esteja atualmente desenhado na janela
        self.limpar_janela()
        # Garante que a sessão seja zerada sempre que a tela de login for aberta
        self.usuario_atual = None

        # --- SELETOR DE IDIOMAS ---
        # Cria um menu suspenso (ComboBox) para o usuário selecionar o idioma do sistema
        combo_idioma_login = ctk.CTkComboBox(
            self.janela, 
            values=list(self.mapa_idiomas.keys()), # Obtém as chaves do dicionário de idiomas disponíveis
            command=self.mudar_idioma_na_tela_login, # Define a função disparada ao trocar a seleção
            width=120
        )
        # Cria um dicionário reverso para encontrar o nome legível do idioma a partir da sigla atual
        idioma_invertido = {v: k for k, v in self.mapa_idiomas.items()}
        # Define o texto inicial do ComboBox baseado no idioma ativo no tradutor (padrão: Português)
        combo_idioma_login.set(idioma_invertido.get(_.IDIOMA_ATUAL, "Português"))
        # Posiciona o seletor no canto superior direito da janela
        combo_idioma_login.place(relx=0.95, rely=0.03, anchor="ne") 
        
        # --- BOTÃO DE SAIR DA APLICAÇÃO ---
        # Cria um botão vermelho estilizado dedicado a encerrar a aplicação
        btn_sair_sistema = ctk.CTkButton(
            self.janela,
            text=_.t("btn_sair") if hasattr(_, 't') else "Sair", # Tenta traduzir, se falhar exibe "Sair"
            width=80,
            height=28,
            fg_color="#E74C3C",       # Cor de fundo vermelho elegante (código hexadecimal)
            hover_color="#C0392B",    # Cor vermelha ligeiramente mais escura ao passar o mouse (hover)
            font=("Roboto", 12, "bold"),
            command=self.janela.quit  # Comando nativo do Tkinter para fechar a aplicação
        )
        # Posiciona o botão de sair logo abaixo do seletor de idiomas, também à direita
        btn_sair_sistema.place(relx=0.95, rely=0.09, anchor="ne")
        # ---------------------------------

        # Cria um contêiner (Frame) com fundo transparente para abrigar o logo/título principal
        logo_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        logo_frame.pack(pady=(40, 10)) # Adiciona margem vertical externa no posicionamento

        # Título principal da tela, estilizado e com suporte a método de tradução _.t()
        titulo = ctk.CTkLabel(logo_frame, text=_.t("titulo_login"), font=("Roboto", 32, "bold"), text_color=self.ACCENT_GOLD)
        titulo.pack()

        # Cria o quadro (Frame) principal centralizado que atuará como "cartão" de login
        frame = ctk.CTkFrame(self.janela, width=400, height=450, corner_radius=12, fg_color=self.CARD_BG)
        frame.pack(pady=20)
        frame.pack_propagate(False) # Impede que o frame se redimensione automaticamente para se ajustar aos filhos

        # Subtítulo com instrução ou boas-vindas
        subtitulo = ctk.CTkLabel(frame, text=_.t("subtitulo_login"), font=("Roboto", 14, "bold"), text_color=self.TEXT_MUTED)
        subtitulo.pack(pady=(30, 20))

        # Campo de entrada para captura do e-mail do usuário
        self.entry_email = ctk.CTkEntry(
            frame, width=300, height=38, 
            placeholder_text=_.t("campo_email"), # Texto de dica (placeholder) que some ao digitar
            corner_radius=8
        )
        self.entry_email.pack(pady=10)

        # Campo de entrada para a senha
        self.entry_senha = ctk.CTkEntry(
            frame, width=300, height=38, 
            placeholder_text=_.t("campo_senha"), 
            show="*", # A propriedade 'show' oculta os caracteres digitados por questões de segurança
            corner_radius=8
        )
        self.entry_senha.pack(pady=10)

        # Caixa de seleção (Checkbox) opcional para exibir a senha digitada
        self.check_mostrar_senha = ctk.CTkCheckBox(
            frame, text=_.t("mostrar_senha"), 
            command=self.toggle_senha # Dispara a função que altera a visibilidade ao ser clicada
        )
        self.check_mostrar_senha.pack(pady=(5, 15))

        # Botão principal de ação para confirmar o login
        btn_entrar = ctk.CTkButton(
            frame, width=300, height=40, 
            text=_.t("btn_entrar"), 
            font=("Roboto", 14, "bold"), 
            fg_color=self.COR_PRINCIPAL, 
            command=self.realizar_login # Vincula o botão à lógica de validação
        )
        btn_entrar.pack(pady=10)

        # Etiqueta de texto simples sugerindo o cadastro para novos usuários
        ctk.CTkLabel(frame, text="Ainda não é cliente?", font=("Roboto", 12), text_color=self.TEXT_MUTED).pack(pady=(15, 0))
        
        # Botão secundário de ação para redirecionar o usuário para o formulário de cadastro
        btn_ir_cadastro = ctk.CTkButton(
            frame, width=300, height=35, 
            text="Criar nova conta", 
            fg_color="transparent", border_width=1, border_color=self.COR_PRINCIPAL, text_color=self.COR_PRINCIPAL,
            command=self.tela_cadastro # Dispara a função de construção da tela de cadastro
        )
        btn_ir_cadastro.pack(pady=5)

    def mudar_idioma_na_tela_login(self, idioma_escolhido):
        """
        Função que atua como gatilho da caixa de seleção de idiomas.

        Args:
            idioma_escolhido (str): O nome legível do idioma selecionado no ComboBox.
        """
        # Busca no dicionário a sigla associada ao idioma escolhido (ex: 'Inglês' -> 'en')
        sigla = self.mapa_idiomas.get(idioma_escolhido, "pt")
        # Invoca a classe Tradutor para atualizar o idioma base em tempo de execução
        _.mudar_idioma(sigla)
        # Reconstrói a tela de login do zero para aplicar imediatamente a nova linguagem
        self.tela_login()

    def tela_cadastro(self):
        """
        Constrói e exibe a interface de registro de novos usuários na tela.
        """
        # Remove os elementos da interface de login para limpar a tela
        self.limpar_janela()

        # Título da tela de cadastro formatado
        titulo = ctk.CTkLabel(self.janela, text="Seja um Gestor EasyFinance", font=("Roboto", 28, "bold"), text_color=self.ACCENT_GOLD)
        titulo.pack(pady=(40, 20))

        # Contêiner central para o formulário de criação de conta
        frame = ctk.CTkFrame(self.janela, width=400, height=500, corner_radius=12, fg_color=self.CARD_BG)
        frame.pack()
        frame.pack_propagate(False) # Trava o tamanho do contêiner

        # Subtítulo explicativo
        ctk.CTkLabel(frame, text="Preencha seus dados corporativos", font=("Roboto", 14), text_color=self.TEXT_MUTED).pack(pady=(20, 20))

        # Campo para inserir o e-mail que será cadastrado
        self.entry_email_cad = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Seu melhor E-mail corporativo", corner_radius=8)
        self.entry_email_cad.pack(pady=10)

        # Campo para inserir a nova senha, com o texto mascarado
        self.entry_senha_cad = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Crie uma Senha Forte", show="*", corner_radius=8)
        self.entry_senha_cad.pack(pady=10)

        # Botão para submeter os dados e concluir a criação da conta
        btn_criar = ctk.CTkButton(
            frame, width=300, height=40, text="Cadastrar e Acessar", font=("Roboto", 14, "bold"), 
            fg_color="#2ecc71", hover_color="#27ae60", # Botão de sucesso em tonalidades verdes
            command=self.realizar_cadastro # Vinculado à lógica de criação de usuário
        )
        btn_criar.pack(pady=(20, 10))

        # Etiqueta de texto caso o usuário já tenha registro
        ctk.CTkLabel(frame, text="Já possui conta?", font=("Roboto", 12), text_color=self.TEXT_MUTED).pack(pady=(15, 0))
        
        # Botão para retornar ao painel de login inicial
        btn_voltar = ctk.CTkButton(
            frame, width=300, height=35, text="Voltar ao Login", 
            fg_color="transparent", border_width=1, border_color=self.TEXT_MUTED, text_color=self.TEXT_MAIN,
            command=self.tela_login # Recarrega a interface de login
        )
        btn_voltar.pack(pady=5)

    def toggle_senha(self):
        """
        Alterna a visibilidade do texto no campo de senha da tela de login.
        Oculta com '*' ou mostra os caracteres reais baseado na interação do usuário.
        """
        # Garante de forma segura que a variável de entrada de senha foi instanciada
        if self.entry_senha:
            # Obtém a propriedade atual que define se o texto está visível ou não
            current_show = self.entry_senha.cget("show")
            
            # Se a senha estiver escondida (exibindo asteriscos)
            if current_show == "*":
                # Remove o bloqueio visual para mostrar os caracteres
                self.entry_senha.configure(show="")
            # Caso contrário (se já estiver visível)
            else:
                # Retorna os asteriscos para ocultar os caracteres
                self.entry_senha.configure(show="*")

    def realizar_login(self):
        """
        Coleta as credenciais da interface e executa o fluxo completo de autenticação.
        Se os dados base passarem, aciona o envio e verificação do 2FA (código de e-mail) 
        antes de dar acesso ao painel interno.
        """
        # Puxa o que foi digitado nas caixas de texto.
        # O .strip() no e-mail previne que espaços em branco gerem erros de formatação
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()

        # Importações locais usadas apenas para a manipulação dos alertas (pop-ups)
        import tkinter.messagebox as messagebox
        import customtkinter as ctk  
        
        # 1. Tenta validar o e-mail e a senha utilizando a camada de serviço (Service)
        # Retorna um status de sucesso (True/False) e o objeto do usuário (ou mensagem de erro)
        sucesso, resultado = self.auth_service.realizar_login(email, senha)
        
        if sucesso:
            # 2. Em caso de senha e e-mail corretos, solicita ao serviço o envio do e-mail de 2FA
            codigo_enviado = self.auth_service.enviar_2fa_email(email)
            
            # Valida se o serviço conseguiu enviar o e-mail com sucesso
            if codigo_enviado:
                # 3. Abre uma pequena janela de diálogo sobreposta para o usuário inserir o token
                dialogo = ctk.CTkInputDialog(
                    text="Um código de segurança foi enviado ao seu e-mail.\n\nDigite o código de 6 dígitos:", 
                    title="Autenticação de Dois Fatores (2FA)"
                )
                codigo_usuario = dialogo.get_input() # Para a execução e aguarda a entrada do usuário
                
                # 4. Compara o código que o usuário digitou com o gerado/enviado pelo sistema
                if codigo_usuario == codigo_enviado:
                    # Configura a sessão informando o usuário validado na aplicação
                    self.usuario_atual = resultado
                    
                    # 5. Instancia a janela principal de trabalho (Painel)
                    painel = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
                    painel.usuario_atual = self.usuario_atual # Transfere os dados da sessão do usuário
                    painel.tela_dashboard() # Executa a renderização do dashboard
                else:
                    # Caso o token 2FA seja diferente, bloqueia o acesso
                    messagebox.showerror("Acesso Negado", "Código de segurança incorreto. Login cancelado.")
            else:
                # Trata erros de infraestrutura caso o e-mail falhe em ser despachado
                messagebox.showerror("Erro de Envio", "Não foi possível enviar o e-mail de 2FA.\nVerifique suas credenciais de e-mail no .env ou sua conexão.")
        else:
            # Informa o usuário caso ele tenha digitado as credenciais erradas na primeira etapa
            messagebox.showerror("Acesso Negado", resultado)

    def realizar_cadastro(self):
        """
        Inicia o processo de registro de um novo usuário.
        Coleta as entradas da tela de cadastro e aplica regras de segurança através 
        de validadores externos (Expressões Regulares - Regex) antes de criar a conta.
        """
        # Captura os dados digitados e remove eventuais espaços das extremidades do e-mail
        email = self.entry_email_cad.get().strip()
        senha = self.entry_senha_cad.get()

        # Importações feitas internamente ao escopo da função para exibir pop-ups e regras
        import tkinter.messagebox as messagebox
        from src.utils.validators import validar_email, validar_senha

        # Checa as regras de e-mail usando funções utilitárias importadas
        if not validar_email(email):
            # Trava o fluxo e notifica o usuário sobre o padrão de preenchimento esperado
            messagebox.showwarning("E-mail Inválido", "O formato do e-mail inserido é inválido. \nExemplo aceito: contato@empresa.com.br")
            return # Interrompe a execução da função aqui
            
        # Analisa a força da senha digitada via Regex
        if not validar_senha(senha):
            # Notifica o usuário detalhando exatamente quais são as métricas mínimas para registrar a senha
            messagebox.showwarning("Senha Fraca", "Sua senha deve conter:\n- Pelo menos 7 caracteres\n- 1 Letra Maiúscula\n- 1 Número\n- 1 Caractere Especial (@$!%*?&.)")
            return # Interrompe a execução da função aqui
            
        # NOTA DE IMPLEMENTAÇÃO: Após estas validações de segurança da interface,
        # O código precisa ser despachado para a camada de serviços criar o usuário (Ex: self.auth_service.criar_usuario...)