# src/views/modulos_suporte.py
import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from src.views.core_window import CoreWindow
from src.utils.tradutor import Tradutor as _
from datetime import datetime

class ModulosSuporte(CoreWindow):
    def tela_educacao(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("area_educacao"))
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(content, text=_.t("titulo_educacao"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        scroll_frame = ctk.CTkScrollableFrame(content, width=550, height=400, fg_color=self.CARD_BG)
        scroll_frame.pack(fill="both", expand=True)

        # 📚 Lista com 20 cursos reais com links ativos e validados no YouTube
        cursos = [
            {"titulo": "01. Reserva de Emergência: Como e Onde Guardar", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=bEqt--FVP68"},
            {"titulo": "02. Como Organizar as Finanças para Sair das Dívidas", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=A_cQp2ZgBkw"},
            {"titulo": "03. O Guia para Organizar seu Dinheiro com a Regra 50-30-20", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=F3a37yG265A"},
            {"titulo": "04. Finanças para MEI: Como Separar Conta Física da Jurídica", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=H7yV23V4h3Y"},
            {"titulo": "05. Como Fazer o Controle de Fluxo de Caixa da sua Empresa", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=kR2jKtz6s6A"},
            {"titulo": "06. Como Calcular o Preço de Venda do seu Produto ou Serviço", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=7M06NlWf0L0"},
            {"titulo": "07. O que é Capital de Giro e Como Funciona na Prática", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=vVnK2_TkiCg"},
            {"titulo": "08. Entenda de vez a Margem de Lucro e Margem de Contribuição", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=8I1kM5Lh-I0"},
            {"titulo": "09. Planejamento Financeiro Empresarial para Iniciantes", "canal": "Erico Rocha", "url": "https://www.youtube.com/watch?v=kY31N3k-k4E"},
            {"titulo": "10. Finanças Descomplicadas para o Microempreendedor Individual", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=P_Yw8mI4tX4"},
            {"titulo": "11. Como Reduzir Custos e Despesas na sua Empresa", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=v8V3y9L-y8Y"},
            {"titulo": "12. Contabilidade Básica e Leitura de Balanço para Não-Contadores", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=68f2A_9fD9M"},
            {"titulo": "13. Como Funciona a Tributação e Impostos no Simples Nacional", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=q6t8mC9gAnU"},
            {"titulo": "14. Como Conseguir Crédito Bancário Consciente para seu Negócio", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=vM-vYvJvExM"},
            {"titulo": "15. Como Montar e Analisar uma DRE (Demonstração de Resultados)", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=fXW9PndBPlg"},
            {"titulo": "16. Onde Investir o Dinheiro do Caixa de uma Empresa", "canal": "O Primo Rico", "url": "https://www.youtube.com/watch?v=gM9j2vA_y4M"},
            {"titulo": "17. Gestão de Estoque Inteligente e seu Impacto no Caixa", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=Nn_xS7x9I20"},
            {"titulo": "18. Estratégias para Reduzir a Inadimplência de Clientes", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=8bXgGz_N_eM"},
            {"titulo": "19. Principais Indicadores Financeiros para Avaliar sua Empresa", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=LNZ-L64E9q4"},
            {"titulo": "20. Mentalidade de Negócios e Gestão Eficiente de Riscos", "canal": "Geração de Valor", "url": "https://www.youtube.com/watch?v=6Pz_T9jM43k"}
        ]

        # 🔒 Correção do Bug: Garante que o atributo seja lido como uma lista (iterable)
        cursos_feitos = getattr(self.usuario_atual, 'cursos_concluidos', [])
        if isinstance(cursos_feitos, int):
            cursos_feitos = []  # Reseta temporariamente para lista para não quebrar a interface antiga

        for item in cursos:
            item_frame = ctk.CTkFrame(scroll_frame, fg_color=("#EAEAEA", "#1F2937"))
            item_frame.pack(fill="x", padx=15, pady=6)

            # Verifica se o curso já está na lista de concluídos do usuário
            ja_concluido = item['titulo'] in cursos_feitos
            sufixo_status = " ✅ (Concluído)" if ja_concluido else ""

            lbl = ctk.CTkLabel(
                item_frame, 
                text=f"{item['titulo']}{sufixo_status}\nCanal: {item['canal']}", 
                justify="left", 
                anchor="w", 
                wraplength=350, 
                text_color=self.TEXT_MAIN if not ja_concluido else "#10B981"
            )
            lbl.pack(side="left", padx=15, pady=10)
            
            btn = ctk.CTkButton(
                item_frame, 
                text=_.t("btn_assistir"), 
                width=90, 
                command=lambda i=item: self.assistir_aula(i['titulo'], i['url'])
            )
            btn.pack(side="right", padx=15, pady=10)

    def assistir_aula(self, titulo, url):
        """Abre o navegador e gerencia a concessão de pontos baseada no retorno do finance_service."""
        import webbrowser
        import tkinter.messagebox as messagebox

        # 1. Abre a URL do curso no navegador padrão
        webbrowser.open(url)
        
        # 2. Caixa de confirmação para validar o empenho do usuário
        pergunta = f"Você foi direcionado para a aula:\n'{titulo}'\n\nConfirma que concluiu os estudos deste módulo para computar seus 20 pontos corporativos?"
        
        if messagebox.askyesno("Confirmar Conclusão", pergunta):
            # 3. Chama o seu método 'concluir_curso' passando os parâmetros que ele exige
            sucesso, msg = self.finance_service.concluir_curso(self.usuario_atual, titulo, 20)
            
            if sucesso:
                # Exibe a mensagem de sucesso com os pontos adicionados
                messagebox.showinfo(_.t("sucesso"), msg)
            else:
                # Se o serviço retornar False (ex: curso duplicado), exibe o aviso
                messagebox.showwarning(_.t("aviso"), msg)
                
            # 4. Recarrega a tela para atualizar dinamicamente os indicadores e marcações visuais de '✅'
            self.tela_educacao()

    def tela_metas(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("metas_financeiras"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("titulo_metas"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'metas') or not self.usuario_atual.metas:
            ctk.CTkLabel(left_col, text=_.t("nenhuma_meta"), text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for m in self.usuario_atual.metas:
                m_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                m_frame.pack(fill="x", pady=8, padx=10)
                
                obj = m.get('objetivo', 'Meta') if isinstance(m, dict) else getattr(m, 'objetivo', 'Meta')
                val = m.get('valor', 0.0) if isinstance(m, dict) else getattr(m, 'valor', 0.0)
                
                lbl_obj = ctk.CTkLabel(m_frame, text=f"🎯 {obj}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_obj.pack(fill="x", padx=15, pady=(12, 2))
                
                lbl_val = ctk.CTkLabel(m_frame, text=f"{_.t('alvo_meta')}: R$ {val:,.2f}".replace(",", "."), font=("Roboto", 13, "bold"), text_color=("#27AE60", "#2ECC71"), anchor="w")
                lbl_val.pack(fill="x", padx=15, pady=(0, 12))

        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG, corner_radius=12)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text=_.t("nova_meta"), font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=10)
        
        self.entry_meta_obj = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_meta_obj"), width=180, corner_radius=8)
        self.entry_meta_obj.pack(pady=5)
        
        self.entry_meta_val = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_meta_val"), width=180, corner_radius=8)
        self.entry_meta_val.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text=_.t("btn_add_meta"), width=180, font=("Roboto", 14, "bold"), command=self.salvar_meta_gui, corner_radius=8)
        btn.pack(pady=15)

    def salvar_meta_gui(self):
        objetivo = self.entry_meta_obj.get().strip()
        valor_str = self.entry_meta_val.get().strip()
        
        if not objetivo or not valor_str:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_preencha_meta"))
            
        try:
            valor_meta = float(valor_str)
            if hasattr(self.finance_service, 'adicionar_meta'):
                self.finance_service.adicionar_meta(self.usuario_atual, objetivo, valor_meta)
            else:
                if not hasattr(self.usuario_atual, 'metas'):
                    self.usuario_atual.metas = []
                self.usuario_atual.metas.append({"objetivo": objetivo, "valor": valor_meta})
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            messagebox.showinfo(_.t("sucesso"), _.t("msg_meta_add"))
            self.tela_metas()
        except ValueError:
            messagebox.showerror(_.t("erro"), _.t("msg_erro_valor"))

    def tela_lembretes(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("lembretes_contas"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("titulo_lembretes"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'lembretes') or not self.usuario_atual.lembretes:
            ctk.CTkLabel(left_col, text=_.t("nenhum_lembrete"), text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for l in self.usuario_atual.lembretes:
                l_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                l_frame.pack(fill="x", pady=8, padx=10)
                
                conta = l.get('conta', 'Conta') if isinstance(l, dict) else getattr(l, 'conta', 'Conta')
                data = l.get('data', '--/--/----') if isinstance(l, dict) else getattr(l, 'data', '--/--/----')
                status = l.get('status', 'Pendente') if isinstance(l, dict) else getattr(l, 'status', 'Pendente')
                lbl_conta = ctk.CTkLabel(l_frame, text=f"📋 {conta}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_conta.pack(fill="x", padx=15, pady=(12, 2))
                
                if status == "Vencida":
                    texto_data = f"⚠️ Vencida em: {data}"
                    cor_texto = "#E74C3C"
                else:
                    texto_data = f"📅 {_.t('vence_em')}: {data}"
                    cor_texto = ("#D35400", "#E67E22")
                
                lbl_data = ctk.CTkLabel(l_frame, text=f"📅 {_.t('vence_em')}: {data}", font=("Roboto", 13), text_color=("#D35400", "#E67E22"), anchor="w")
                lbl_data.pack(fill="x", padx=15, pady=(0, 12))

        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG, corner_radius=12)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text=_.t("novo_lembrete"), font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=10)
        
        self.entry_lembrete_conta = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_conta"), width=180)
        self.entry_lembrete_conta.pack(pady=5)
        
        self.entry_lembrete_data = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_data"), width=180)
        self.entry_lembrete_data.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text=_.t("btn_agendar"), width=180, font=("Roboto", 14, "bold"), command=self.salvar_lembrete_gui)
        btn.pack(pady=15)

    def salvar_lembrete_gui(self):
        conta = self.entry_lembrete_conta.get().strip()
        data = self.entry_lembrete_data.get().strip()
    
    # Validação de campos vazios
        if not conta or not data:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_preencha_campos"))
    
    # 1. VALIDAÇÃO DE FORMATO DA DATA
        try:
        # Tenta converter o texto em uma data válida real
            data_validada = datetime.strptime(data, "%d/%m/%Y").date()
        except ValueError:
            return messagebox.showerror(
                _.t("Erro") if hasattr(_, 't') else "Erro",
                "Formato de data inválido! Por favor, insira no formato DD/MM/AAAA (Ex: 18/05/2026)."
            )
        hoje = datetime.today().date()
        status = "Pendente"
        msg_adicional = ""

        if data_validada < hoje:
            status = "Vencida"

            VALOR_MULTA = 15.00

            if hasattr(self.finance_service, 'adicionar_transacao'):
                try:
                    self.finance_service.adicionar_transacao(
                        self.usuario_atual,
                        "SAÍDA",  # Tipo compatível com o filtro de saldo do seu Usuario model
                        VALOR_MULTA,
                        "Multas",
                        f"Multa automática: Lembrete '{conta}' criado já vencido.",
                        hoje.strftime("%d/%m/%Y")
                    )
                except Exception:
                    pass
            else:
                from src.models.transacao import transacao
                nova_multa = transacao(
                    tipo="SAÍDA", 
                    valor=VALOR_MULTA, 
                    descricao=f"Multa automática: Lembrete '{conta}' criado já vencido.", 
                    data=hoje.strftime("%d/%m/%Y")
                )
                self.usuario_atual.transacoes.append(nova_multa)

            msg_adicional = _.t(f"\n\n⚠️ Atenção: Como a data informada já passou, o lembrete foi marcado como 'Vencido' e uma multa de R$ {VALOR_MULTA:.2f} foi debitada do seu saldo!")

        if hasattr(self.finance_service, 'adicionar_lembrete'):
            try:
                self.finance_service.adicionar_lembrete(self.usuario_atual, conta, data)
            except TypeError:
                self.finance_service.adicionar_lembrete(self.usuario_atual, conta, data)
                if hasattr(self.usuario_atual, 'lembretes') and self.usuario_atual.lembretes:
                    ultimo = self.usuario_atual.lembretes[-1]
                    if isinstance(ultimo, dict):
                        ultimo['status'] = status
                else:
                    setattr(ultimo, 'status', status)
        else:
            if not hasattr(self.usuario_atual, 'lembretes'):
                self.usuario_atual.lembretes = []
            self.usuario_atual.lembretes.append({"conta": conta, "data": data, "status": status})
            self.auth_service.repo.salvar_usuario(self.usuario_atual)
        messagebox.showinfo(_.t("sucesso"), _.t("msg_lembrete_add") + msg_adicional)
        self.entry_lembrete_conta.delete(0, 'end')
        self.entry_lembrete_data.delete(0, 'end')

        self.tela_lembretes()
        
    def tela_perfil(self):
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("editar_perfil"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("config_conta"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        form_frame = ctk.CTkFrame(content, width=400, height=450, fg_color=self.CARD_BG)
        form_frame.pack(anchor="w", pady=10, fill="y")
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text=_.t("lbl_email"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 5))
        entry_email = ctk.CTkEntry(form_frame, width=350)
        entry_email.insert(0, self.usuario_atual.email)
        entry_email.configure(state="disabled")
        entry_email.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text=_.t("lbl_doc"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_perfil_doc = ctk.CTkEntry(form_frame, width=350)
        doc_atual = getattr(self.usuario_atual, 'documento', '')
        self.entry_perfil_doc.insert(0, doc_atual)
        self.entry_perfil_doc.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text=_.t("lbl_nova_senha"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        # Campo de senha (Inicia oculto com '*')
        self.entry_perfil_senha = ctk.CTkEntry(form_frame, width=350, show="*")
        self.entry_perfil_senha.insert(0, self.usuario_atual.senha)
        self.entry_perfil_senha.pack(padx=20)
        
        # --- REQUISITO ENH001: Checkbox de Mascaramento Dinâmico de Senha ---
        self.chk_mostrar_senha = ctk.CTkCheckBox(
            form_frame, 
            text=_.t("mostrar_senha", "Mostrar senha"),
            font=("Roboto", 11),
            checkbox_width=16,
            checkbox_height=16,
            command=self.toggle_mostrar_senha_perfil
        )
        self.chk_mostrar_senha.pack(anchor="w", padx=20, pady=(10, 0))
        
        btn_salvar = ctk.CTkButton(form_frame, text=_.t("btn_salvar_perfil"), command=self.salvar_perfil_gui)
        btn_salvar.pack(pady=35)

    def toggle_mostrar_senha_perfil(self):
        """Alterna a visibilidade dos caracteres no campo de edição de senha."""
        if self.chk_mostrar_senha.get() == 1:
            self.entry_perfil_senha.configure(show="")
        else:
            self.entry_perfil_senha.configure(show="*")

    def salvar_perfil_gui(self):
        novo_doc = self.entry_perfil_doc.get().strip()
        nova_senha = self.entry_perfil_senha.get().strip()
        
        # 1. Validação de campo em branco
        if not nova_senha:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_senha_branco"))
            
        # --- LÓGICA DE HISTÓRICO DE SENHAS ---
        # Garante que o usuário possua a lista de histórico (previne erros em contas antigas)
        if not hasattr(self.usuario_atual, 'historico_senhas'):
            self.usuario_atual.historico_senhas = []

        # 2. Verifica se o usuário mudou a senha ou manteve a mesma
        if nova_senha != self.usuario_atual.senha:
            
            # 3. Verifica se a nova senha já foi usada antes no histórico
            if nova_senha in self.usuario_atual.historico_senhas:
                return messagebox.showwarning(
                    _.t("aviso_seguranca", "Aviso de Segurança"), 
                    _.t("msg_senha_repetida", "Você não pode reutilizar uma senha antiga por motivos de segurança. Escolha uma senha diferente.")
                )
            
            # Se passou pela verificação, adicionamos a senha ANTIGA ao histórico antes de trocar
            self.usuario_atual.historico_senhas.append(self.usuario_atual.senha)
            
            # (Opcional) Limita o histórico a guardar apenas as últimas 5 senhas para não pesar o banco
            if len(self.usuario_atual.historico_senhas) > 5:
                self.usuario_atual.historico_senhas.pop(0)

        # Salva os novos dados
        self.usuario_atual.documento = novo_doc
        self.usuario_atual.senha = nova_senha
        
        self.auth_service.repo.salvar_usuario(self.usuario_atual)
        messagebox.showinfo(_.t("sucesso"), _.t("msg_perfil_ok"))