# src/views/login_cadastro.py
import customtkinter as ctk
from src.views.core_window import CoreWindow
from src.views.painel_financeiro import PainelFinanceiro
from src.utils.tradutor import Tradutor as _

class LoginCadastro(CoreWindow):
    def __init__(self, auth_service, finance_service, janela=None):
        super().__init__(auth_service, finance_service, janela)
        self.entry_senha = None
        self.check_mostrar_senha = None
        self.entry_email = None
        self.entry_senha_cad = None

    def tela_login(self):
        self.limpar_janela()
        self.usuario_atual = None

        # --- SELETOR DE IDIOMAS ---
        combo_idioma_login = ctk.CTkComboBox(
            self.janela, 
            values=list(self.mapa_idiomas.keys()), 
            command=self.mudar_idioma_na_tela_login,
            width=120
        )
        idioma_invertido = {v: k for k, v in self.mapa_idiomas.items()}
        combo_idioma_login.set(idioma_invertido.get(_.IDIOMA_ATUAL, "Português"))
        combo_idioma_login.place(relx=0.95, rely=0.03, anchor="ne") # Subi um pouquinho
        
        # --- BOTÃO DE SAIR DA APLICAÇÃO (Adicionado/Recuperado) ---
        btn_sair_sistema = ctk.CTkButton(
            self.janela,
            text=_.t("btn_sair") if hasattr(_, 't') else "Sair",
            width=80,
            height=28,
            fg_color="#E74C3C",       # Vermelho elegante
            hover_color="#C0392B", # Vermelho mais escuro no hover
            font=("Roboto", 12, "bold"),
            command=self.janela.quit # Fecha o programa de vez
        )
        # Posicionado logo abaixo do seletor de idiomas no canto direito
        btn_sair_sistema.place(relx=0.95, rely=0.09, anchor="ne")
        # ---------------------------------

        logo_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        logo_frame.pack(pady=(40, 10))

        # Strings com _.t() para tradução
        titulo = ctk.CTkLabel(logo_frame, text=_.t("titulo_login"), font=("Roboto", 32, "bold"), text_color=self.ACCENT_GOLD)
        titulo.pack()

        frame = ctk.CTkFrame(self.janela, width=400, height=450, corner_radius=12, fg_color=self.CARD_BG)
        frame.pack(pady=20)
        frame.pack_propagate(False)

        subtitulo = ctk.CTkLabel(frame, text=_.t("subtitulo_login"), font=("Roboto", 14, "bold"), text_color=self.TEXT_MUTED)
        subtitulo.pack(pady=(30, 20))

        self.entry_email = ctk.CTkEntry(
            frame, width=300, height=38, 
            placeholder_text=_.t("campo_email"), 
            corner_radius=8
        )
        self.entry_email.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(
            frame, width=300, height=38, 
            placeholder_text=_.t("campo_senha"), 
            show="*", corner_radius=8
        )
        self.entry_senha.pack(pady=10)

        self.check_mostrar_senha = ctk.CTkCheckBox(
            frame, text=_.t("mostrar_senha"), 
            command=self.toggle_senha
        )
        self.check_mostrar_senha.pack(pady=(5, 15))

        btn_entrar = ctk.CTkButton(
            frame, width=300, height=40, 
            text=_.t("btn_entrar"), 
            font=("Roboto", 14, "bold"), 
            fg_color=self.COR_PRINCIPAL, 
            command=self.realizar_login
        )
        btn_entrar.pack(pady=10)

        # Adicionei chaves genéricas de tradução ou deixei em PT para o cadastro
        ctk.CTkLabel(frame, text="Ainda não é cliente?", font=("Roboto", 12), text_color=self.TEXT_MUTED).pack(pady=(15, 0))
        btn_ir_cadastro = ctk.CTkButton(
            frame, width=300, height=35, 
            text="Criar nova conta", 
            fg_color="transparent", border_width=1, border_color=self.COR_PRINCIPAL, text_color=self.COR_PRINCIPAL,
            command=self.tela_cadastro
        )
        btn_ir_cadastro.pack(pady=5)

    def mudar_idioma_na_tela_login(self, idioma_escolhido):
        """Função que gerencia o gatilho da caixa de idiomas"""
        sigla = self.mapa_idiomas.get(idioma_escolhido, "pt")
        _.mudar_idioma(sigla)
        self.tela_login()

    def tela_cadastro(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self.janela, text="Seja um Gestor EasyFinance", font=("Roboto", 28, "bold"), text_color=self.ACCENT_GOLD)
        titulo.pack(pady=(40, 20))

        # Dica: Aumentei um pouquinho a altura do frame para 530 para caber o novo campo confortavelmente
        frame = ctk.CTkFrame(self.janela, width=400, height=530, corner_radius=12, fg_color=self.CARD_BG)
        frame.pack()
        frame.pack_propagate(False)

        ctk.CTkLabel(frame, text="Preencha seus dados corporativos", font=("Roboto", 14), text_color=self.TEXT_MUTED).pack(pady=(20, 20))

        self.entry_email_cad = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Seu melhor E-mail corporativo", corner_radius=8)
        self.entry_email_cad.pack(pady=10)

        # 🔽 NOVO CAMPO ADICIONADO AQUI 🔽
        self.entry_documento_cad = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="CNPJ ou CPF Corporativo", corner_radius=8)
        self.entry_documento_cad.pack(pady=10)

        self.entry_senha_cad = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Crie uma Senha Forte", show="*", corner_radius=8)
        self.entry_senha_cad.pack(pady=10)

        btn_criar = ctk.CTkButton(
            frame, width=300, height=40, text="Cadastrar e Acessar", font=("Roboto", 14, "bold"), 
            fg_color="#2ecc71", hover_color="#27ae60",
            command=self.realizar_cadastro
        )
        btn_criar.pack(pady=(20, 10))

        ctk.CTkLabel(frame, text="Já possui conta?", font=("Roboto", 12), text_color=self.TEXT_MUTED).pack(pady=(15, 0))
        btn_voltar = ctk.CTkButton(
            frame, width=300, height=35, text="Voltar ao Login", 
            fg_color="transparent", border_width=1, border_color=self.TEXT_MUTED, text_color=self.TEXT_MAIN,
            command=self.tela_login
        )
        btn_voltar.pack(pady=5)

    def toggle_senha(self):
        """Alterna a visibilidade da senha na tela de login."""
        if self.entry_senha:
            current_show = self.entry_senha.cget("show")
            if current_show == "*":
                self.entry_senha.configure(show="")
            else:
                self.entry_senha.configure(show="*")

    def realizar_login(self):
        """Chama o service de autenticação. Se passar, envia o 2FA antes de ir para o painel."""
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()

        import tkinter.messagebox as messagebox
        import customtkinter as ctk  # Importamos para usar a caixinha de input do 2FA
        
        # 1. Valida e-mail e senha no banco de dados
        sucesso, resultado = self.auth_service.realizar_login(email, senha)
        
        if sucesso:
            # 2. Se a senha estiver certa, dispara o e-mail com o código de 2FA
            codigo_enviado = self.auth_service.enviar_2fa_email(email)
            
            if codigo_enviado:
                # 3. Abre a caixinha popup perguntando o código para o usuário
                dialogo = ctk.CTkInputDialog(
                    text="Um código de segurança foi enviado ao seu e-mail.\n\nDigite o código de 6 dígitos:", 
                    title="Autenticação de Dois Fatores (2FA)"
                )
                codigo_usuario = dialogo.get_input()
                
                # 4. Verifica se o código digitado é igual ao enviado por e-mail
                if codigo_usuario == codigo_enviado:
                    self.usuario_atual = resultado
                    
                    # Se o código estiver certo, aí sim abre o Painel Principal
                    painel = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
                    painel.usuario_atual = self.usuario_atual
                    painel.tela_dashboard()
                else:
                    messagebox.showerror("Acesso Negado", "Código de segurança incorreto. Login cancelado.")
            else:
                messagebox.showerror("Erro de Envio", "Não foi possível enviar o e-mail de 2FA.\nVerifique suas credenciais de e-mail no .env ou sua conexão.")
        else:
            messagebox.showerror("Acesso Negado", resultado)
    def realizar_cadastro(self):
        """Registra um novo gestor usando as lógicas de segurança e regex."""
        email = self.entry_email_cad.get().strip()
        documento = self.entry_documento_cad.get().strip() # 🔽 CAPTURA O DOCUMENTO
        senha = self.entry_senha_cad.get()

        import tkinter.messagebox as messagebox
        from src.utils.validators import validar_email, validar_senha

        if not validar_email(email):
            messagebox.showwarning("E-mail Inválido", "O formato do e-mail inserido é inválido. \nExemplo aceito: contato@empresa.com.br")
            return
            
        # (Opcional) Você pode criar uma validação para o documento aqui se quiser
        if not documento:
            messagebox.showwarning("Documento Ausente", "Por favor, insira o seu CNPJ ou CPF.")
            return

        if not validar_senha(senha):
            messagebox.showwarning("Senha Fraca", "Sua senha deve conter:\n- Pelo menos 7 caracteres\n- 1 Letra Maiúscula\n- 1 Número\n- 1 Caractere Especial (@$!%*?&.)")
            return

        try:
            # 🔽 AGORA PASSAMOS OS 3 PARÂMETROS NA ORDEM CORRETA 🔽
            sucesso, mensagem = self.auth_service.cadastrar_usuario(email, documento, senha)
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

                self.entry_email_cad.delete(0, 'end')
                self.entry_documento_cad.delete(0, 'end') # Limpa o novo campo
                self.entry_senha_cad.delete(0, 'end')
                
                self.tela_login()
            else:
                messagebox.showwarning("Erro no Cadastro", mensagem)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar cadastro: {e}")