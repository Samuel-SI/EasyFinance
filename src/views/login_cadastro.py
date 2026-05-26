# src/views/login_cadastro.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import re
from src.views.core_window import CoreWindow

class LoginCadastro(CoreWindow):
    def tela_login(self):
        self.limpar_janela()
        self.usuario_atual = None

        try:
            imagem_logo = ctk.CTkImage(light_image=Image.open("logo.png"), dark_image=Image.open("logo.png"), size=(120, 120))
            lbl_logo = ctk.CTkLabel(self.janela, image=imagem_logo, text="")
            lbl_logo.pack(pady=(20, 0))
        except:
            pass 

        titulo = ctk.CTkLabel(self.janela, text="Bem vindo ao EasyFinance", font=("Roboto", 28, "bold"), text_color=self.ACCENT_GOLD)
        titulo.pack(pady=(20, 30))

        frame = ctk.CTkFrame(self.janela, width=400, height=400, corner_radius=12, fg_color=self.CARD_BG)
        frame.place(relx=0.5, rely=0.55, anchor="center")
        frame.pack_propagate(False)

        subtitulo = ctk.CTkLabel(frame, text="Acesse sua Conta Corporativa", font=("Roboto", 14, "bold"), text_color=self.TEXT_MUTED)
        subtitulo.pack(pady=(30, 20))

        self.entry_email = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Digite seu e-mail:", corner_radius=8, fg_color=("#F1F5F9", "#1F2937"), border_color=("#CBD5E1", "#374151"))
        self.entry_email.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(frame, width=300, height=38, placeholder_text="Digite sua senha:", show="*", corner_radius=8, fg_color=("#F1F5F9", "#1F2937"), border_color=("#CBD5E1", "#374151"))
        self.entry_senha.pack(pady=10)

        self.check_mostrar_senha = ctk.CTkCheckBox(frame, text="Mostrar Senha", command=self.toggle_senha, font=("Roboto", 12), text_color=self.TEXT_MUTED)
        self.check_mostrar_senha.pack(pady=5)

        btn_entrar = ctk.CTkButton(frame, width=300, height=40, text="Entrar no sistema", font=("Roboto", 14, "bold"), command=self.processar_login, corner_radius=8)
        btn_entrar.pack(pady=(25, 15))

        btn_cadastrar = ctk.CTkButton(frame, width=300, height=35, text="Criar nova conta", fg_color="transparent", border_width=2, text_color=self.COR_PRINCIPAL, corner_radius=8, command=self.tela_cadastro)
        btn_cadastrar.pack(pady=5)

    def processar_login(self):
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
            
        sucesso, resultado = self.auth_service.realizar_login(email, senha) # Nota: assumindo a injeção correta do serviço

        if sucesso:
            usuario = resultado
            codigo_enviado = self.auth_service.enviar_2fa_email(usuario.email)
            
            if not codigo_enviado:
                messagebox.showerror("Erro", "Não foi possível enviar o código 2FA.")
                return

            dialog = ctk.CTkInputDialog(text=f"Código enviado para {usuario.email}.\nDigite o código 2FA:", title="Segurança")
            codigo_digitado = dialog.get_input()
            
            if codigo_digitado and codigo_digitado.strip() == codigo_enviado:
                self.usuario_atual = usuario
                from src.views.painel_financeiro import PainelFinanceiro
                dashboard = PainelFinanceiro(self.auth_service, self.finance_service, self.janela)
                dashboard.sincronizar_usuario(self)
                dashboard.tela_dashboard()
            else:
                messagebox.showerror("Acesso Negado", "Código 2FA incorreto ou cancelado.")
        else:
            messagebox.showerror("Erro", resultado)

    def tela_cadastro(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self.janela, text="Nova Conta Corporativa", font=("Roboto", 28, "bold"), text_color=self.COR_PRINCIPAL)
        titulo.pack(pady=(50, 20))

        frame = ctk.CTkFrame(self.janela, width=400, height=450, fg_color=self.CARD_BG)
        frame.place(relx=0.5, rely=0.55, anchor="center")
        frame.pack_propagate(False)

        ctk.CTkLabel(frame, text="Preencha os dados da sua empresa", font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=(25, 15))

        self.reg_email = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="E-mail (ex: contato@empresa.com)")
        self.reg_email.pack(pady=10)

        self.reg_doc = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="CNPJ ou CPF (apenas números)")
        self.reg_doc.pack(pady=10)

        self.reg_senha = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="Senha (Mín. 8 chars, letras e números)", show="*")
        self.reg_senha.pack(pady=10)

        btn_salvar = ctk.CTkButton(frame, width=300, height=40, text="Cadastrar Empresa", command=self.processar_cadastro)
        btn_salvar.pack(pady=(25, 10))

        btn_voltar = ctk.CTkButton(frame, width=300, height=35, text="Voltar ao Login", fg_color="transparent", text_color="gray", command=self.tela_login)
        btn_voltar.pack(pady=5)

    def processar_cadastro(self):
        email = self.reg_email.get().strip()
        doc = self.reg_doc.get().strip()
        senha = self.reg_senha.get().strip()

        if not email or not doc or not senha:
            return messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return messagebox.showerror("Erro de Validação", "O e-mail digitado não é válido.")

        doc_limpo = re.sub(r"[^\d]", "", doc)
        if not re.match(r"^(\d{11}|\d{14})$", doc_limpo):
            return messagebox.showerror("Erro de Validação", "O documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).")

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", senha):
            return messagebox.showerror("Erro de Validação", "A senha deve ter no mínimo 8 caracteres, contendo letras e números.")

        sucesso, msg = self.auth_service.cadastrar_usuario(email, doc_limpo, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça login.")
            self.tela_login()
        else:
            messagebox.showerror("Erro", msg)

    def toggle_senha(self):
        if self.check_mostrar_senha.get() == 1:
            self.entry_senha.configure(show="")
        else:
            self.entry_senha.configure(show="*")