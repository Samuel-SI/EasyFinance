import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from PIL import Image
import re


class GuiView:
    def __init__(self, auth_service, finance_service):
        self.auth_service = auth_service
        self.finance_service = finance_service
        self.usuario_atual = None

        # 🪐 Configuração de Aparência Global
        ctk.set_appearance_mode("dark")  # Deixa o app no modo escuro profundo por padrão
        
        # 🎨 Nova Paleta Premium (Estrutura de Tuplas: M. Claro, M. Escuro)
        self.APP_BG = ("#F8FAFC", "#0B0F19")        # Azul Meia-Noite Profundo
        self.CARD_BG = ("#FFFFFF", "#111827")       # Cards Grafite Fechado
        self.PRIMARY = ("#1E3A8A", "#6366F1")       # Índigo de Alta Tecnologia
        self.ACCENT_GOLD = ("#9A3412", "#F59E0B")   # Ouro Champagne (Luxo)
        self.TEXT_MAIN = ("#0F172A", "#F1F5F9")     # Texto Ultra Nítido
        self.TEXT_MUTED = ("#64748B", "#94A3B8")    # Texto de suporte (cinza elegante)
        
        # Ponte de segurança: Atualiza seu código antigo para a nova cor sem quebrar nada!
        self.COR_PRINCIPAL = self.PRIMARY 

        # 🪟 Inicialização e Dimensionamento da Janela
        self.janela = ctk.CTk()
        self.janela.geometry("950x650")
        self.janela.title("EasyFinance - Gestão de Negócios B2B")
        
        # Aplica o tom escuro de luxo diretamente no fundo da janela principal
        self.janela.configure(fg_color=self.APP_BG)

        # Abre o sistema
        self.tela_login()

    def limpar_janela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def tela_login(self):
        self.limpar_janela()

        try:
            imagem_logo = ctk.CTkImage(
                light_image=Image.open("logo.png"), 
                dark_image=Image.open("logo.png"), 
                size=(120, 120)
            )
            lbl_logo = ctk.CTkLabel(self.janela, image=imagem_logo, text="")
            lbl_logo.pack(pady=(20, 0))
        except:
            pass 

        # NOVO TÍTULO PREMIUM (Ouro Champagne sobre fundo meia-noite - VISÍVEL!)
        titulo = ctk.CTkLabel(
            self.janela, 
            text="Bem vindo ao EasyFinance", 
            font=("Roboto", 28, "bold"), 
            text_color=self.ACCENT_GOLD # Usando Ouro Champagne
        )
        titulo.pack(pady=(20, 30)) # Mais espaçamento

        # FRAME DE LOGIN (Centralizado e Grafite Fechado)
        frame = ctk.CTkFrame(
            self.janela, 
            width=400, 
            height=400, 
            corner_radius=12,
            fg_color=self.CARD_BG # Usando Grafite Fechado
        )
        frame.place(relx=0.5, rely=0.55, anchor="center")
        frame.pack_propagate(False)

        subtitulo = ctk.CTkLabel(frame, text="Acesse sua Conta Corporativa", font=("Roboto", 14, "bold"), text_color=self.TEXT_MUTED)
        subtitulo.pack(pady=(30, 20))

        # Campos de entrada discretos e com bordas finas
        self.entry_email = ctk.CTkEntry(
            frame, 
            width=300, 
            height=38, 
            placeholder_text="Digite seu e-mail:",
            corner_radius=8,
            fg_color=("#F1F5F9", "#1F2937"),
            border_color=("#CBD5E1", "#374151")
        )
        self.entry_email.pack(pady=10)

        self.entry_senha = ctk.CTkEntry(
            frame, 
            width=300, 
            height=38, 
            placeholder_text="Digite sua senha:", 
            show="*",
            corner_radius=8,
            fg_color=("#F1F5F9", "#1F2937"),
            border_color=("#CBD5E1", "#374151")
        )
        self.entry_senha.pack(pady=10)

        # Usando o frame correto para o checkbox
        self.check_mostrar_senha = ctk.CTkCheckBox(
            frame, # MUDAMOS PARA FRAME
            text="Mostrar Senha", 
            command=self.toggle_senha, 
            font=("Roboto", 12),
            text_color=self.TEXT_MUTED
        )
        self.check_mostrar_senha.pack(pady=5)

        # Botão principal em Índigo
        btn_entrar = ctk.CTkButton(frame, width=300, height=40, text="Entrar no sistema", font=("Roboto", 14, "bold"), command=self.processar_login, corner_radius=8)
        btn_entrar.pack(pady=(25, 15))

        # NOVO BOTÃO DE CADASTRO (Transparente corporativo)
        btn_cadastrar = ctk.CTkButton(
            frame, 
            width=300, 
            height=35, 
            text="Criar nova conta", 
            fg_color="transparent", 
            border_width=2, 
            text_color=self.COR_PRINCIPAL, # Usará a ponte COR_PRINCIPAL -> PRIMARY
            corner_radius=8,
            command=self.tela_cadastro
        )
        btn_cadastrar.pack(pady=5)

        # BOTÃO SAIR (Vermelho Suave corporativo)
        btn_sair = ctk.CTkButton(
            frame, 
            width=300, 
            height=35, 
            text="Sair do Aplicativo", 
            fg_color="transparent", 
            text_color="#FF4444", 
            corner_radius=8,
            command=self.janela.destroy
        )
        btn_sair.pack(pady=5)

    def processar_login(self):
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
            
        sucesso, resultado = self.auth_service.realizar_login(email, senha)

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
                self.tela_dashboard()
            else:
                messagebox.showerror("Acesso Negado", "Código 2FA incorreto ou cancelado.")
        else:
            messagebox.showerror("Erro", resultado)

    # ==========================================
    # TELA DE CADASTRO DE NOVO USUÁRIO
    # ==========================================
    def tela_cadastro(self):
        self.limpar_janela()

        titulo = ctk.CTkLabel(self.janela, text="Nova Conta Corporativa", font=("Roboto", 28, "bold"), text_color=self.COR_PRINCIPAL)
        titulo.pack(pady=(50, 20))

        frame = ctk.CTkFrame(self.janela, width=400, height=450)
        frame.place(relx=0.5, rely=0.55, anchor="center")
        frame.pack_propagate(False)

        ctk.CTkLabel(frame, text="Preencha os dados da sua empresa", font=("Roboto", 14, "bold")).pack(pady=(25, 15))

        self.reg_email = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="E-mail (ex: contato@empresa.com)")
        self.reg_email.pack(pady=10)

        self.reg_doc = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="CNPJ ou CPF (apenas números)")
        self.reg_doc.pack(pady=10)

        self.reg_senha = ctk.CTkEntry(frame, width=300, height=35, placeholder_text="Senha (Mín. 8 chars, letras e números)", show="*")
        self.reg_senha.pack(pady=10)

        btn_salvar = ctk.CTkButton(frame, width=300, height=40, text="Cadastrar Empresa", command=self.processar_cadastro)
        btn_salvar.pack(pady=(25, 10))

        btn_voltar = ctk.CTkButton(frame, width=300, height=35, text="Voltar ao Login", fg_color="transparent", text_color="gray", hover_color="#333333", command=self.tela_login)
        btn_voltar.pack(pady=5)

    def processar_cadastro(self):
        email = self.reg_email.get().strip()
        doc = self.reg_doc.get().strip()
        senha = self.reg_senha.get().strip()

        # 1. Verifica se tem campo vazio
        if not email or not doc or not senha:
            return messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")

        # 2. Validação de E-mail com Regex
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return messagebox.showerror("Erro de Validação", "O e-mail digitado não é válido.")

        # 3. Validação de Documento com Regex (Remove formatação e checa se tem 11 ou 14 números)
        doc_limpo = re.sub(r"[^\d]", "", doc)
        if not re.match(r"^(\d{11}|\d{14})$", doc_limpo):
            return messagebox.showerror("Erro de Validação", "O documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).")

        # 4. Validação de Senha com Regex (Mínimo 8 caracteres, pelo menos uma letra e um número)
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", senha):
            return messagebox.showerror("Erro de Validação", "A senha é muito fraca. Ela deve ter no mínimo 8 caracteres, contendo letras e números.")

        # Se passou por todas as validações, tenta registrar no banco de dados!
        sucesso, msg = self.auth_service.cadastrar_usuario(email, doc_limpo, senha)
        
        if sucesso:
            messagebox.showinfo("Sucesso", "Conta criada com sucesso! Faça login para acessar o painel.")
            self.tela_login()
        else:
            messagebox.showerror("Erro", msg)

    def desenhar_menu_lateral(self, aba_ativa):
        sidebar = ctk.CTkFrame(self.janela, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        lbl_menu = ctk.CTkLabel(sidebar, text="EASYFINANCE", font=("Roboto", 20, "bold"), text_color=self.COR_PRINCIPAL)
        lbl_menu.pack(pady=30)

        # Atualizado com as novas abas
        abas = [
            ("Painel Principal", self.tela_dashboard),
            ("Balanço Geral", self.tela_balanco),
            ("Diagnóstico Financeiro", self.tela_diagnostico),
            ("Área de Educação", self.tela_educacao),
            ("Metas Financeiras", self.tela_metas),
            ("Lembretes de Contas", self.tela_lembretes),
            ("Editar Perfil", self.tela_perfil)
        ]

        for nome, comando in abas:
            cor_botao = self.COR_PRINCIPAL if nome == aba_ativa else "transparent"
            btn = ctk.CTkButton(sidebar, text=nome, fg_color=cor_botao, anchor="w", command=comando)
            btn.pack(fill="x", padx=10, pady=5)

        btn_sair = ctk.CTkButton(sidebar, text="Sair", fg_color="#c0392b", hover_color="#962d22", command=self.tela_login)
        btn_sair.pack(side="bottom", fill="x", padx=10, pady=20)

    # ==========================================
    # TELA 1: NOVO DASHBOARD FINANCEIRO
    # ==========================================
    def tela_dashboard(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Painel Principal")

        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(content, text="Painel Principal", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))

        # Cálculos financeiros baseados nas transações
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo_atual = total_receitas - total_despesas

        # Fileira 1: Cartões Financeiros
        financas_frame = ctk.CTkFrame(content, fg_color="transparent")
        financas_frame.pack(fill="x", pady=10)

        self.criar_card(financas_frame, "Saldo Atual", f"R$ {saldo_atual:.2f}", "#2ecc71" if saldo_atual >= 0 else "#e74c3c")
        self.criar_card(financas_frame, "Receitas do Mês", f"R$ {total_receitas:.2f}", self.COR_PRINCIPAL)
        self.criar_card(financas_frame, "Despesas do Mês", f"R$ {total_despesas:.2f}", "#e74c3c")

        ctk.CTkLabel(content, text="Seu Desempenho B2B", font=("Roboto", 18, "bold")).pack(anchor="w", pady=(20, 10))

        # Fileira 2: Gamificação
        gamifica_frame = ctk.CTkFrame(content, fg_color="transparent")
        gamifica_frame.pack(fill="x", pady=10)

        self.criar_card(gamifica_frame, "Sua Pontuação Técnica", f"{self.usuario_atual.pontos} XP", "#f1c40f")
        self.criar_card(gamifica_frame, "Nível do Perfil", f"{self.usuario_atual.ranking}", "#9b59b6")

    def criar_card(self, parent, titulo, valor, cor_valor):
        """Função auxiliar para desenhar cartões padronizados"""
        card = ctk.CTkFrame(parent, width=220, height=100)
        card.pack(side="left", padx=(0, 15))
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=titulo, font=("Roboto", 14)).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=valor, font=("Roboto", 22, "bold"), text_color=cor_valor).pack()

    # ==========================================
    # TELA 2: BALANÇO GERAL (Lista de Transações)
    # ==========================================
    def tela_balanco(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Balanço Geral")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Fluxo de Caixa e Transações", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=400, height=400)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        if not transacoes:
            ctk.CTkLabel(left_col, text="Nenhuma transação registrada.", text_color="gray").pack(pady=20)
        else:
            for t in reversed(transacoes): # Mostra as mais recentes primeiro
                t_frame = ctk.CTkFrame(left_col)
                t_frame.pack(fill="x", pady=4, padx=5)
                
                desc = t.get('descricao', '') if isinstance(t, dict) else getattr(t, 'descricao', '')
                valor = t.get('valor', 0.0) if isinstance(t, dict) else getattr(t, 'valor', 0.0)
                tipo = t.get('tipo', '') if isinstance(t, dict) else getattr(t, 'tipo', '')
                
                cor = "#2ecc71" if tipo == "Receita" else "#e74c3c"
                sinal = "+" if tipo == "Receita" else "-"
                
                ctk.CTkLabel(t_frame, text=f"{desc}", font=("Roboto", 14, "bold")).pack(side="left", padx=15, pady=10)
                ctk.CTkLabel(t_frame, text=f"{sinal} R$ {float(valor):.2f}", text_color=cor, font=("Roboto", 14, "bold")).pack(side="right", padx=15, pady=10)

        # Formulário para Nova Transação
        right_col = ctk.CTkFrame(content, width=220)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text="Nova Movimentação", font=("Roboto", 16, "bold")).pack(pady=15)
        
        self.combo_tipo_transacao = ctk.CTkComboBox(right_col, values=["Receita", "Despesa"], width=180)
        self.combo_tipo_transacao.pack(pady=5)
        
        self.entry_desc_transacao = ctk.CTkEntry(right_col, placeholder_text="Descrição (Ex: Venda)", width=180)
        self.entry_desc_transacao.pack(pady=5)
        
        self.entry_valor_transacao = ctk.CTkEntry(right_col, placeholder_text="Valor (Ex: 1500.00)", width=180)
        self.entry_valor_transacao.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text="Registrar", width=180, command=self.salvar_transacao_gui)
        btn.pack(pady=20)

    def salvar_transacao_gui(self):
        tipo = self.combo_tipo_transacao.get()
        desc = self.entry_desc_transacao.get().strip()
        valor_str = self.entry_valor_transacao.get().strip()
        
        if not desc or not valor_str:
            return messagebox.showwarning("Aviso", "Preencha a descrição e o valor.")
            
        try:
            valor = float(valor_str)
            if hasattr(self.finance_service, 'adicionar_transacao'):
                # CORREÇÃO AQUI: A ordem agora é (usuario, tipo, valor, desc)
                self.finance_service.adicionar_transacao(self.usuario_atual, tipo, valor, desc)
            else:
                if not hasattr(self.usuario_atual, 'transacoes'):
                    self.usuario_atual.transacoes = []
                self.usuario_atual.transacoes.append({"tipo": tipo, "descricao": desc, "valor": valor})
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            messagebox.showinfo("Sucesso", "Transação registrada!")
            self.tela_balanco()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")

    # ==========================================
    # TELA 3: DIAGNÓSTICO FINANCEIRO
    # ==========================================
    def tela_diagnostico(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Diagnóstico Financeiro")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Relatório de Saúde Financeira", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Cálculos
        transacoes = getattr(self.usuario_atual, 'transacoes', [])
        total_receitas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Receita')
        total_despesas = sum(float(t.get('valor', 0)) if isinstance(t, dict) else float(getattr(t, 'valor', 0)) for t in transacoes if (t.get('tipo') if isinstance(t, dict) else getattr(t, 'tipo', '')) == 'Despesa')
        saldo = total_receitas - total_despesas
        
        diag_frame = ctk.CTkFrame(content, corner_radius=10)
        diag_frame.pack(fill="both", expand=True, pady=10)
        
        if saldo > 0:
            status = "SAUDÁVEL 🟢"
            msg = "Parabéns! Sua empresa está operando no azul. Suas receitas superam as despesas.\nRecomendação: Considere investir o dinheiro excedente para criar uma reserva de emergência."
            cor = "#2ecc71"
        elif saldo < 0:
            status = "EM ALERTA 🔴"
            msg = "Atenção! Sua empresa está gastando mais do que arrecada.\nRecomendação: Revise a aba de 'Balanço Geral' e corte despesas não essenciais imediatamente."
            cor = "#e74c3c"
        else:
            status = "ESTÁVEL 🟡"
            msg = "Sua empresa não tem lucros nem prejuízos no momento.\nRecomendação: Foque em aumentar as vendas ou criar novas fontes de receita."
            cor = "#f1c40f"
            
        ctk.CTkLabel(diag_frame, text=f"Status Atual: {status}", font=("Roboto", 22, "bold"), text_color=cor).pack(pady=(40, 20))
        ctk.CTkLabel(diag_frame, text=msg, font=("Roboto", 16), wraplength=500, justify="center").pack(pady=20)

    # ==========================================
    # TELA 4: EDITAR PERFIL
    # ==========================================
    def tela_perfil(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Editar Perfil")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Configurações da Conta", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))
        
        form_frame = ctk.CTkFrame(content, width=400, height=400)
        form_frame.pack(anchor="w", pady=10, fill="y")
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="E-mail (Login):", font=("Roboto", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
        entry_email = ctk.CTkEntry(form_frame, width=350)
        entry_email.insert(0, self.usuario_atual.email)
        entry_email.configure(state="disabled") # Email não deve ser alterado pois é a chave primária
        entry_email.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text="Documento (CNPJ/CPF):", font=("Roboto", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_perfil_doc = ctk.CTkEntry(form_frame, width=350)
        doc_atual = getattr(self.usuario_atual, 'documento', '')
        self.entry_perfil_doc.insert(0, doc_atual)
        self.entry_perfil_doc.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text="Nova Senha:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_perfil_senha = ctk.CTkEntry(form_frame, width=350, show="*")
        self.entry_perfil_senha.insert(0, self.usuario_atual.senha)
        self.entry_perfil_senha.pack(padx=20)
        
        btn_salvar = ctk.CTkButton(form_frame, text="Salvar Alterações", command=self.salvar_perfil_gui)
        btn_salvar.pack(pady=40)

    def salvar_perfil_gui(self):
        novo_doc = self.entry_perfil_doc.get().strip()
        nova_senha = self.entry_perfil_senha.get().strip()
        
        if not nova_senha:
            return messagebox.showwarning("Aviso", "A senha não pode ficar em branco.")
            
        self.usuario_atual.documento = novo_doc
        self.usuario_atual.senha = nova_senha
        
        # Salva as alterações no banco JSON
        self.auth_service.repo.salvar_usuario(self.usuario_atual)
        messagebox.showinfo("Sucesso", "Dados do perfil atualizados com sucesso!")

    # ==========================================
    # AS OUTRAS TELAS CONTINUAM INTACTAS
    # ==========================================
    def tela_educacao(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Área de Educação")
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(content, text="EasyFinance Academy", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))
        
        scroll_frame = ctk.CTkScrollableFrame(content, width=550, height=400)
        scroll_frame.pack(fill="both", expand=True)

        cursos = [
            # 🟢 Educação Financeira Básica e Reserva
            {"titulo": "O que é e como fazer uma Reserva de Emergência", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=UqN69zVn2q0"},
            {"titulo": "Como Organizar suas Finanças e Sair das Dívidas", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=A_cQp2ZgBkw"},
            {"titulo": "A regra 50-30-20 para organizar o seu dinheiro", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=F3a37yG265A"},
            {"titulo": "Onde Investir 100 Reais Hoje? (Prática)", "canal": "Gêmeos Investidores", "url": "https://www.youtube.com/watch?v=3IeP9R7oAt8"},
            {"titulo": "Como começar a investir do ZERO", "canal": "O Primo Rico", "url": "https://www.youtube.com/watch?v=84E11oxD3Bw"},
            
            # 🔵 Gestão de Negócios e MEI
            {"titulo": "Como Separar a Conta Física da Jurídica", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=H7yV23V4h3Y"},
            {"titulo": "Controle de Fluxo de Caixa para Pequenos Negócios", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=kR2jKtz6s6A"},
            {"titulo": "Como Abrir um MEI Passo a Passo", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=9g0H7H6zR_M"},
            {"titulo": "Como Precificar o seu Produto ou Serviço", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=P6Yy2rO27lM"},
            {"titulo": "Impostos para MEI: O que você precisa pagar", "canal": "Contabilidade Facilitada", "url": "https://www.youtube.com/watch?v=9_7P86uI0j0"},
            {"titulo": "Os 3 Erros Fatais que Quebram Qualquer Empresa", "canal": "Jovens de Negócios", "url": "https://www.youtube.com/watch?v=687pL-C9Zms"},
            
            # 🟠 Investimentos e Renda Fixa (Para o caixa da empresa)
            {"titulo": "Como Funciona o Tesouro Direto na Prática", "canal": "Você MAIS Rico", "url": "https://www.youtube.com/watch?v=Vl03C8vD84E"},
            {"titulo": "O que são CDBs e como investir neles", "canal": "Economirna", "url": "https://www.youtube.com/watch?v=uT3wN62E2-w"},
            {"titulo": "Fundos Imobiliários (FIIs) para Iniciantes", "canal": "Clube do Valor", "url": "https://www.youtube.com/watch?v=KzXgZ4uVnqw"},
            {"titulo": "Ações: Como analisar uma empresa antes de investir", "canal": "Canal do Holder", "url": "https://www.youtube.com/watch?v=1K5_0P8fOQ8"},
            
            # 🟣 Mentalidade Empreendedora e Vendas
            {"titulo": "Psicologia do Dinheiro: Como sua Mente te Deixa Pobre", "canal": "IlustradaMente", "url": "https://www.youtube.com/watch?v=P_D652yT_bY"},
            {"titulo": "Como Vender Mais usando a Internet", "canal": "Erico Rocha", "url": "https://www.youtube.com/watch?v=I4w3bO_f5y4"},
            {"titulo": "A Visão de Águia nos Negócios", "canal": "Rick Chesther", "url": "https://www.youtube.com/watch?v=7h7K9U7_8jE"},
            {"titulo": "Geração de Valor: Como pensar grande", "canal": "Flávio Augusto", "url": "https://www.youtube.com/watch?v=7X5X8oW8e_4"},
            {"titulo": "Livros de Finanças que Todo Empreendedor Deve Ler", "canal": "Gustavo Cerbasi", "url": "https://www.youtube.com/watch?v=1rA-YQf6n_0"},
            
            # 🟤 Ferramentas e Dicas Práticas
            {"titulo": "Como fazer o Imposto de Renda (IRPF)", "canal": "Contadora da Bolsa", "url": "https://www.youtube.com/watch?v=3g6HqW1bBcw"},
            {"titulo": "Melhores Cartões de Crédito para MEI", "canal": "Favelado Investidor", "url": "https://www.youtube.com/watch?v=2rZ_n7kHkQo"},
            {"titulo": "Como Reduzir Custos na sua Empresa de forma inteligente", "canal": "Patricia Lages", "url": "https://www.youtube.com/watch?v=4M_3aY_zE-w"}
        ]

        for item in cursos:
            item_frame = ctk.CTkFrame(scroll_frame)
            item_frame.pack(fill="x", padx=15, pady=6)

            lbl = ctk.CTkLabel(item_frame, text=f"{item['titulo']}\nCanal: {item['canal']}", justify="left", anchor="w", wraplength=350)
            lbl.pack(side="left", padx=15, pady=10)
            btn = ctk.CTkButton(item_frame, text="Assistir", width=90, command=lambda i=item: self.assistir_aula(i['titulo'], i['url']))
            btn.pack(side="right", padx=15, pady=10)

    def assistir_aula(self, titulo, url):
        webbrowser.open(url)
        sucesso, msg = self.finance_service.concluir_curso(self.usuario_atual, titulo, 20)
        if sucesso: messagebox.showinfo("Sucesso!", msg)
        else: messagebox.showwarning("Aviso", msg)
        self.tela_educacao()

    def tela_metas(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Metas Financeiras")
        
        # Painel principal do conteúdo
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Título da tela principal em Branco Nítido
        ctk.CTkLabel(content, text="Metas e Objetivos do Negócio", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # Coluna da Esquerda (Lista de Metas com fundo Grafite Fechado)
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'metas') or not self.usuario_atual.metas:
            ctk.CTkLabel(left_col, text="Nenhuma meta cadastrada.", text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for m in self.usuario_atual.metas:
                # Card com cantos arredondados e cores para os modos claro/escuro
                # CORREÇÃO: Usando a COR_PRINCIPAL antiga ou constantes novas
                m_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B")) # Adicionei o '#' que faltava no 2B2B2B
                m_frame.pack(fill="x", pady=8, padx=10)
                
                obj = m.get('objetivo', 'Meta') if isinstance(m, dict) else getattr(m, 'objetivo', 'Meta')
                val = m.get('valor', 0.0) if isinstance(m, dict) else getattr(m, 'valor', 0.0)
                
                # Texto 1: O Objetivo (Maior, em Negrito, e em Branco Nítido - VISÍVEL!)
                lbl_obj = ctk.CTkLabel(
                    m_frame, 
                    text=f"🎯 {obj}", 
                    font=("Roboto", 16, "bold"), 
                    text_color=self.TEXT_MAIN, # Garantindo que contraste com o card
                    anchor="w"
                )
                lbl_obj.pack(fill="x", padx=15, pady=(12, 2))
                
                # Texto 2: O Valor Alvo (Verde de destaque com formatação correta de milhar)
                lbl_val = ctk.CTkLabel(
                    m_frame, 
                    text=f"Alvo: R$ {val:,.2f}".replace(",", "."), 
                    font=("Roboto", 13, "bold"), 
                    text_color=("#27AE60", "#2ECC71"), # Verde vibrante
                    anchor="w"
                )
                lbl_val.pack(fill="x", padx=15, pady=(0, 12))

        # Coluna da Direita (Formulário de Nova Meta)
        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG, corner_radius=12)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text="Nova Meta", font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=10)
        
        self.entry_meta_obj = ctk.CTkEntry(right_col, placeholder_text="Ex: Novo Servidor", width=180, corner_radius=8)
        self.entry_meta_obj.pack(pady=5)
        
        self.entry_meta_val = ctk.CTkEntry(right_col, placeholder_text="Ex: 5000.00", width=180, corner_radius=8)
        self.entry_meta_val.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text="Adicionar Meta", width=180, font=("Roboto", 14, "bold"), command=self.salvar_meta_gui, corner_radius=8)
        btn.pack(pady=15)

    def salvar_meta_gui(self):
        objetivo = self.entry_meta_obj.get().strip()
        valor_str = self.entry_meta_val.get().strip()
        
        # 1. Validação simples de campos vazios
        if not objetivo or not valor_str:
            return messagebox.showwarning("Aviso", "Preencha o objetivo e o valor da meta.")
            
        try:
            # 2. Conversão crucial do texto para número decimal (float)
            valor_meta = float(valor_str)
            
            # 3. Chama o serviço passando os dados
            if hasattr(self.finance_service, 'adicionar_meta'):
                self.finance_service.adicionar_meta(self.usuario_atual, objetivo, valor_meta)
            else:
                # Fallback de segurança
                if not hasattr(self.usuario_atual, 'metas'):
                    self.usuario_atual.metas = []
                self.usuario_atual.metas.append({"objetivo": objetivo, "valor": valor_meta})
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            messagebox.showinfo("Sucesso", "Meta financeira adicionada!")
            self.tela_metas() # Recarrega a tela para mostrar a nova meta na lista
            
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido para o alvo (Ex: 1500.50).")

    def tela_lembretes(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Lembretes de Contas")
        
        # Painel principal do conteúdo
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Título principal da tela
        ctk.CTkLabel(content, text="Lembretes de Contas a Pagar", font=("Roboto", 24, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Coluna da Esquerda (Lista de Lembretes)
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'lembretes') or not self.usuario_atual.lembretes:
            ctk.CTkLabel(left_col, text="Nenhum compromisso agendado.", text_color="gray").pack(pady=20)
        else:
            for l in self.usuario_atual.lembretes:
                # Card moderno com cantos arredondados e suporte a tema claro/escuro
                l_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                l_frame.pack(fill="x", pady=8, padx=10)
                
                conta = l.get('conta', 'Conta') if isinstance(l, dict) else getattr(l, 'conta', 'Conta')
                data = l.get('data', '--/--/----') if isinstance(l, dict) else getattr(l, 'data', '--/--/----')
                
                # Texto 1: O Compromisso/Conta (Destacado, maior e em negrito)
                lbl_conta = ctk.CTkLabel(
                    l_frame, 
                    text=f"📋 {conta}", 
                    font=("Roboto", 16, "bold"), 
                    anchor="w"
                )
                lbl_conta.pack(fill="x", padx=15, pady=(12, 2))
                
                # Texto 2: A Data de Vencimento (Laranja vibrante para dar senso de urgência)
                lbl_data = ctk.CTkLabel(
                    l_frame, 
                    text=f"📅 Vence em: {data}", 
                    font=("Roboto", 13), 
                    text_color=("#D35400", "#E67E22"),
                    anchor="w"
                )
                lbl_data.pack(fill="x", padx=15, pady=(0, 12))

        # Coluna da Direita (Formulário de Novo Lembrete)
        right_col = ctk.CTkFrame(content, width=220)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text="Novo Lembrete", font=("Roboto", 14, "bold")).pack(pady=10)
        
        self.entry_lembrete_conta = ctk.CTkEntry(right_col, placeholder_text="Ex: Conta de Luz", width=180)
        self.entry_lembrete_conta.pack(pady=5)
        
        self.entry_lembrete_data = ctk.CTkEntry(right_col, placeholder_text="Ex: 10/06/2026", width=180)
        self.entry_lembrete_data.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text="Agendar Conta", width=180, command=self.salvar_lembrete_gui)
        btn.pack(pady=15)

    def salvar_lembrete_gui(self):
        conta = self.entry_lembrete_conta.get().strip()
        data = self.entry_lembrete_data.get().strip()
        
        if not conta or not data:
            return messagebox.showwarning("Aviso", "Preencha a descrição da conta e a data de vencimento.")
            
        # Como ambos os dados são textos (strings), não precisamos fazer conversão com float()!
        if hasattr(self.finance_service, 'adicionar_lembrete'):
            self.finance_service.adicionar_lembrete(self.usuario_atual, conta, data)
        else:
            if not hasattr(self.usuario_atual, 'lembretes'):
                self.usuario_atual.lembretes = []
            self.usuario_atual.lembretes.append({"conta": conta, "data": data})
            self.auth_service.repo.salvar_usuario(self.usuario_atual)
            
        messagebox.showinfo("Sucesso", "Lembrete de conta agendado!")
        self.tela_lembretes()
        
    def toggle_senha(self):
        """Alterna a visibilidade da senha com base no checkbox."""
        # Se o checkbox estiver marcado (get() retorna 1)
        if self.check_mostrar_senha.get() == 1:
            self.entry_senha.configure(show="")  # Remove o "*" e mostra o texto limpo
        else:
            self.entry_senha.configure(show="*")  # Recarrega a tela para atualizar a lista visível

    def iniciar(self):
        self.janela.mainloop()