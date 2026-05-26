# src/views/modulos_suporte.py
import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from src.views.core_window import CoreWindow

class ModulosSuporte(CoreWindow):
    def tela_educacao(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Área de Educação")
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        ctk.CTkLabel(content, text="EasyFinance Academy - 20 Cursos Disponíveis", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        scroll_frame = ctk.CTkScrollableFrame(content, width=550, height=400, fg_color=self.CARD_BG)
        scroll_frame.pack(fill="both", expand=True)

        # 📚 Lista expandida com exatamente 20 cursos estratégicos
        cursos = [
            {"titulo": "01. O que é e como fazer uma Reserva de Emergência", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=UqN69zVn2q0"},
            {"titulo": "02. Como Organizar suas Finanças e Sair das Dívidas", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=A_cQp2ZgBkw"},
            {"titulo": "03. A regra 50-30-20 para organizar o seu dinheiro", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=F3a37yG265A"},
            {"titulo": "04. Como Separar a Conta Física da Jurídica", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=H7yV23V4h3Y"},
            {"titulo": "05. Controle de Fluxo de Caixa para Pequenos Negócios", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=kR2jKtz6s6A"},
            {"titulo": "06. Como Calcular o Preço de Venda do seu Produto/Serviço", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=7M06NlWf0L0"},
            {"titulo": "07. O que é Capital de Giro e como calcular", "canal": "Me Poupe! Negócios", "url": "https://www.youtube.com/watch?v=vVnK2_TkiCg"},
            {"titulo": "08. Margem de Lucro vs Margem de Contribuição", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=8I1kM5Lh-I0"},
            {"titulo": "09. Como Fazer o Planejamento Financeiro Anual da Empresa", "canal": "Erico Rocha", "url": "https://www.youtube.com/watch?v=kY31N3k-k4E"},
            {"titulo": "10. Finanças para Microempreendedor Individual (MEI)", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=P_Yw8mI4tX4"},
            {"titulo": "11. Como Reduzir Custos na sua Empresa Legalmente", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=v8V3y9L-y8Y"},
            {"titulo": "12. Introdução à Contabilidade para Não-Contadores", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=68f2A_9fD9M"},
            {"titulo": "13. Como funciona a tributação Simples Nacional", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=q6t8mC9gAnU"},
            {"titulo": "14. Como Conseguir Crédito Bancário para Empresas", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=vM-vYvJvExM"},
            {"titulo": "15. Análise de Demonstrativo de Resultados (DRE)", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=fXW9PndBPlg"},
            {"titulo": "16. Como Investir o Dinheiro do Caixa da sua Empresa", "canal": "Primo Rico", "url": "https://www.youtube.com/watch?v=gM9j2vA_y4M"},
            {"titulo": "17. Gestão de Estoque e Impacto no Caixa Financeiro", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=Nn_xS7x9I20"},
            {"titulo": "18. Como Evitar a Inadimplência de Clientes B2B", "canal": "Me Poupe! Negócios", "url": "https://www.youtube.com/watch?v=8bXgGz_N_eM"},
            {"titulo": "19. Indicadores Financeiros Práticos que Toda Empresa Precisa", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=LNZ-L64E9q4"},
            {"titulo": "20. Mentalidade Empreendedora e Gestão de Riscos", "canal": "Geração de Valor", "url": "https://www.youtube.com/watch?v=6Pz_T9jM43k"}
        ]

        for item in cursos:
            item_frame = ctk.CTkFrame(scroll_frame, fg_color=("#EAEAEA", "#1F2937"))
            item_frame.pack(fill="x", padx=15, pady=6)

            lbl = ctk.CTkLabel(item_frame, text=f"{item['titulo']}\nCanal: {item['canal']}", justify="left", anchor="w", wraplength=350, text_color=self.TEXT_MAIN)
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
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Metas e Objetivos do Negócio", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'metas') or not self.usuario_atual.metas:
            ctk.CTkLabel(left_col, text="Nenhuma meta cadastrada.", text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for m in self.usuario_atual.metas:
                m_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                m_frame.pack(fill="x", pady=8, padx=10)
                
                obj = m.get('objetivo', 'Meta') if isinstance(m, dict) else getattr(m, 'objetivo', 'Meta')
                val = m.get('valor', 0.0) if isinstance(m, dict) else getattr(m, 'valor', 0.0)
                
                lbl_obj = ctk.CTkLabel(m_frame, text=f"🎯 {obj}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_obj.pack(fill="x", padx=15, pady=(12, 2))
                
                lbl_val = ctk.CTkLabel(m_frame, text=f"Alvo: R$ {val:,.2f}".replace(",", "."), font=("Roboto", 13, "bold"), text_color=("#27AE60", "#2ECC71"), anchor="w")
                lbl_val.pack(fill="x", padx=15, pady=(0, 12))

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
        
        if not objetivo or not valor_str:
            return messagebox.showwarning("Aviso", "Preencha o objetivo e o valor da meta.")
            
        try:
            valor_meta = float(valor_str)
            if hasattr(self.finance_service, 'adicionar_meta'):
                self.finance_service.adicionar_meta(self.usuario_atual, objetivo, valor_meta)
            else:
                if not hasattr(self.usuario_atual, 'metas'):
                    self.usuario_atual.metas = []
                self.usuario_atual.metas.append({"objetivo": objetivo, "valor": valor_meta})
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            messagebox.showinfo("Sucesso", "Meta financeira adicionada!")
            self.tela_metas()
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")

    def tela_lembretes(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Lembretes de Contas")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Lembretes de Contas a Pagar", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        if not hasattr(self.usuario_atual, 'lembretes') or not self.usuario_atual.lembretes:
            ctk.CTkLabel(left_col, text="Nenhum compromisso agendado.", text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for l in self.usuario_atual.lembretes:
                l_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                l_frame.pack(fill="x", pady=8, padx=10)
                
                conta = l.get('conta', 'Conta') if isinstance(l, dict) else getattr(l, 'conta', 'Conta')
                data = l.get('data', '--/--/----') if isinstance(l, dict) else getattr(l, 'data', '--/--/----')
                
                lbl_conta = ctk.CTkLabel(l_frame, text=f"📋 {conta}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_conta.pack(fill="x", padx=15, pady=(12, 2))
                
                lbl_data = ctk.CTkLabel(l_frame, text=f"📅 Vence em: {data}", font=("Roboto", 13), text_color=("#D35400", "#E67E22"), anchor="w")
                lbl_data.pack(fill="x", padx=15, pady=(0, 12))

        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG, corner_radius=12)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text="Novo Lembrete", font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=10)
        
        self.entry_lembrete_conta = ctk.CTkEntry(right_col, placeholder_text="Ex: Conta de Luz", width=180)
        self.entry_lembrete_conta.pack(pady=5)
        
        self.entry_lembrete_data = ctk.CTkEntry(right_col, placeholder_text="Ex: 10/06/2026", width=180)
        self.entry_lembrete_data.pack(pady=5)
        
        btn = ctk.CTkButton(right_col, text="Agendar Conta", width=180, font=("Roboto", 14, "bold"), command=self.salvar_lembrete_gui)
        btn.pack(pady=15)

    def salvar_lembrete_gui(self):
        conta = self.entry_lembrete_conta.get().strip()
        data = self.entry_lembrete_data.get().strip()
        
        if not conta or not data:
            return messagebox.showwarning("Aviso", "Preencha os campos.")
            
        if hasattr(self.finance_service, 'adicionar_lembrete'):
            self.finance_service.adicionar_lembrete(self.usuario_atual, conta, data)
        else:
            if not hasattr(self.usuario_atual, 'lembretes'):
                self.usuario_atual.lembretes = []
            self.usuario_atual.lembretes.append({"conta": conta, "data": data})
            self.auth_service.repo.salvar_usuario(self.usuario_atual)
            
        messagebox.showinfo("Sucesso", "Lembrete agendado!")
        self.tela_lembretes()

    def tela_perfil(self):
        self.limpar_janela()
        self.desenhar_menu_lateral("Editar Perfil")
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text="Configurações da Conta", font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        form_frame = ctk.CTkFrame(content, width=400, height=400, fg_color=self.CARD_BG)
        form_frame.pack(anchor="w", pady=10, fill="y")
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(form_frame, text="E-mail (Login):", font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 5))
        entry_email = ctk.CTkEntry(form_frame, width=350)
        entry_email.insert(0, self.usuario_atual.email)
        entry_email.configure(state="disabled")
        entry_email.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text="Documento (CNPJ/CPF):", font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_perfil_doc = ctk.CTkEntry(form_frame, width=350)
        doc_atual = getattr(self.usuario_atual, 'documento', '')
        self.entry_perfil_doc.insert(0, doc_atual)
        self.entry_perfil_doc.pack(padx=20)
        
        ctk.CTkLabel(form_frame, text="Nova Senha:", font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
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
        self.auth_service.repo.salvar_usuario(self.usuario_atual)
        messagebox.showinfo("Sucesso", "Perfil atualizado!")