# src/views/modulos_suporte.py
"""
Módulo dedicado às funcionalidades de apoio e suporte ao usuário.
Agrupa as telas de Educação Financeira, Metas, Lembretes de Contas e Gestão de Perfil.
"""

import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from src.views.core_window import CoreWindow
from src.utils.tradutor import Tradutor as _

class ModulosSuporte(CoreWindow):
    """
    Classe que gerencia as views secundárias (módulos de suporte) da aplicação.
    Herda de CoreWindow para manter a padronização visual e reaproveitar funcionalidades base.
    """

    def tela_educacao(self):
        """
        Renderiza a interface do módulo de Educação Financeira.
        Exibe uma lista de cursos/aulas em vídeo e permite redirecionamento para o navegador.
        """
        # Prepara a janela limpando conteúdos antigos e redesenhando o menu lateral
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("area_educacao"))
        
        # Cria o contêiner principal para o conteúdo da tela, alinhado à direita
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Título da seção
        ctk.CTkLabel(content, text=_.t("titulo_educacao"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # Cria uma área rolável (ScrollableFrame) para acomodar a longa lista de cursos
        scroll_frame = ctk.CTkScrollableFrame(content, width=550, height=400, fg_color=self.CARD_BG)
        scroll_frame.pack(fill="both", expand=True)

        # 📚 Lista expandida contendo 20 cursos estratégicos pré-definidos (Dicionários com título, canal e URL)
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

        # Itera sobre a lista de cursos para desenhar um item na tela para cada um
        for item in cursos:
            # Cria um sub-frame para cada curso com cor de fundo alternada dependendo do tema (claro/escuro)
            item_frame = ctk.CTkFrame(scroll_frame, fg_color=("#EAEAEA", "#1F2937"))
            item_frame.pack(fill="x", padx=15, pady=6) # Preenche o eixo horizontal

            # Informações de texto do curso (Título e Canal)
            lbl = ctk.CTkLabel(item_frame, text=f"{item['titulo']}\nCanal: {item['canal']}", justify="left", anchor="w", wraplength=350, text_color=self.TEXT_MAIN)
            lbl.pack(side="left", padx=15, pady=10)
            
            # Botão de ação. O lambda 'congela' os dados iterados para que cada botão abra o curso correto
            btn = ctk.CTkButton(item_frame, text=_.t("btn_assistir"), width=90, command=lambda i=item: self.assistir_aula(i['titulo'], i['url']))
            btn.pack(side="right", padx=15, pady=10)

    def assistir_aula(self, titulo, url):
        """
        Abre o vídeo do curso no navegador padrão e tenta registrar a pontuação/conclusão.
        
        Args:
            titulo (str): Título do curso para registro no backend.
            url (str): Link do YouTube a ser aberto.
        """
        # Abre a URL no navegador nativo do sistema operacional do usuário
        webbrowser.open(url)
        
        # Invoca o serviço financeiro/gamificação para registrar que o curso foi acessado
        sucesso, msg = self.finance_service.concluir_curso(self.usuario_atual, titulo, 20)
        
        # Feedback visual ao usuário
        if sucesso: 
            messagebox.showinfo(_.t("sucesso"), msg)
        else: 
            messagebox.showwarning(_.t("aviso"), msg)
            
        # Recarrega a tela para atualizar possíveis pontuações ou status
        self.tela_educacao()

    def tela_metas(self):
        """
        Renderiza a interface de visualização e criação de Metas Financeiras.
        A tela é dividida em uma coluna de listagem (esquerda) e um formulário (direita).
        """
        # Prepara a janela e atualiza o menu lateral para indicar onde o usuário está
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("metas_financeiras"))
        
        # Contêiner principal
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Título da tela
        ctk.CTkLabel(content, text=_.t("titulo_metas"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # --- COLUNA ESQUERDA: LISTAGEM ---
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Verifica se o usuário tem a propriedade 'metas' e se ela não está vazia
        if not hasattr(self.usuario_atual, 'metas') or not self.usuario_atual.metas:
            # Exibe mensagem de estado vazio (Empty State)
            ctk.CTkLabel(left_col, text=_.t("nenhuma_meta"), text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            # Itera sobre cada meta cadastrada
            for m in self.usuario_atual.metas:
                m_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                m_frame.pack(fill="x", pady=8, padx=10)
                
                # Tratamento de compatibilidade: obtém o valor seja a meta um Dicionário ou um Objeto de classe
                obj = m.get('objetivo', 'Meta') if isinstance(m, dict) else getattr(m, 'objetivo', 'Meta')
                val = m.get('valor', 0.0) if isinstance(m, dict) else getattr(m, 'valor', 0.0)
                
                # Exibe o título/objetivo da meta
                lbl_obj = ctk.CTkLabel(m_frame, text=f"🎯 {obj}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_obj.pack(fill="x", padx=15, pady=(12, 2))
                
                # Exibe o valor da meta formatado como moeda (Substitui vírgula por ponto para simplificar a formatação BR)
                lbl_val = ctk.CTkLabel(m_frame, text=f"{_.t('alvo_meta')}: R$ {val:,.2f}".replace(",", "."), font=("Roboto", 13, "bold"), text_color=("#27AE60", "#2ECC71"), anchor="w")
                lbl_val.pack(fill="x", padx=15, pady=(0, 12))

        # --- COLUNA DIREITA: FORMULÁRIO ---
        right_col = ctk.CTkFrame(content, width=220, fg_color=self.CARD_BG, corner_radius=12)
        right_col.pack(side="right", fill="y")
        
        ctk.CTkLabel(right_col, text=_.t("nova_meta"), font=("Roboto", 14, "bold"), text_color=self.TEXT_MAIN).pack(pady=10)
        
        # Campos de entrada de dados para o cadastro da nova meta
        self.entry_meta_obj = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_meta_obj"), width=180, corner_radius=8)
        self.entry_meta_obj.pack(pady=5)
        
        self.entry_meta_val = ctk.CTkEntry(right_col, placeholder_text=_.t("ex_meta_val"), width=180, corner_radius=8)
        self.entry_meta_val.pack(pady=5)
        
        # Botão para invocar a função de salvamento
        btn = ctk.CTkButton(right_col, text=_.t("btn_add_meta"), width=180, font=("Roboto", 14, "bold"), command=self.salvar_meta_gui, corner_radius=8)
        btn.pack(pady=15)

    def salvar_meta_gui(self):
        """
        Captura os dados do formulário de metas, valida a consistência e salva no perfil do usuário.
        """
        # Captura os textos e limpa espaços indesejados no início e no final (strip)
        objetivo = self.entry_meta_obj.get().strip()
        valor_str = self.entry_meta_val.get().strip()
        
        # Bloqueia a submissão se algum campo estiver vazio
        if not objetivo or not valor_str:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_preencha_meta"))
            
        try:
            # Tenta converter o valor digitado em um número decimal (float)
            valor_meta = float(valor_str)
            
            # Se o serviço financeiro estiver pronto para gerir metas (abordagem robusta)
            if hasattr(self.finance_service, 'adicionar_meta'):
                self.finance_service.adicionar_meta(self.usuario_atual, objetivo, valor_meta)
            else:
                # Fallback: Caso o serviço não trate isso, adicionamos diretamente no objeto usuário
                if not hasattr(self.usuario_atual, 'metas'):
                    self.usuario_atual.metas = [] # Cria a lista caso ainda não exista
                self.usuario_atual.metas.append({"objetivo": objetivo, "valor": valor_meta})
                # Persiste as alterações no banco via repositório
                self.auth_service.repo.salvar_usuario(self.usuario_atual)
                
            # Confirma a operação com sucesso e recarrega a interface
            messagebox.showinfo(_.t("sucesso"), _.t("msg_meta_add"))
            self.tela_metas()
        except ValueError:
            # Trata o erro caso o usuário digite texto no campo de valor numérico
            messagebox.showerror(_.t("erro"), _.t("msg_erro_valor"))

    def tela_lembretes(self):
        """
        Renderiza a interface para gerenciamento de Lembretes de Contas a pagar.
        Semelhante estruturalmente à tela de metas: Listagem à esquerda, cadastro à direita.
        """
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("lembretes_contas"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("titulo_lembretes"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # --- COLUNA ESQUERDA: LISTAGEM ---
        left_col = ctk.CTkScrollableFrame(content, width=320, height=350, fg_color=self.CARD_BG, corner_radius=12)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Verifica a existência de lembretes vinculados ao usuário
        if not hasattr(self.usuario_atual, 'lembretes') or not self.usuario_atual.lembretes:
            ctk.CTkLabel(left_col, text=_.t("nenhum_lembrete"), text_color=self.TEXT_MUTED).pack(pady=20)
        else:
            for l in self.usuario_atual.lembretes:
                l_frame = ctk.CTkFrame(left_col, corner_radius=12, fg_color=("#EAEAEA", "#2B2B2B"))
                l_frame.pack(fill="x", pady=8, padx=10)
                
                # Extrai os dados suportando tanto dicionários quanto objetos instanciados
                conta = l.get('conta', 'Conta') if isinstance(l, dict) else getattr(l, 'conta', 'Conta')
                data = l.get('data', '--/--/----') if isinstance(l, dict) else getattr(l, 'data', '--/--/----')
                
                lbl_conta = ctk.CTkLabel(l_frame, text=f"📋 {conta}", font=("Roboto", 16, "bold"), text_color=self.TEXT_MAIN, anchor="w")
                lbl_conta.pack(fill="x", padx=15, pady=(12, 2))
                
                lbl_data = ctk.CTkLabel(l_frame, text=f"📅 {_.t('vence_em')}: {data}", font=("Roboto", 13), text_color=("#D35400", "#E67E22"), anchor="w")
                lbl_data.pack(fill="x", padx=15, pady=(0, 12))

        # --- COLUNA DIREITA: FORMULÁRIO ---
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
        """
        Valida e cadastra um novo lembrete de conta a pagar.
        """
        conta = self.entry_lembrete_conta.get().strip()
        data = self.entry_lembrete_data.get().strip()
        
        # Bloqueio de envio em branco
        if not conta or not data:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_preencha_campos"))
            
        # Trata o armazenamento via service se existir, ou via lista direta se fallback
        if hasattr(self.finance_service, 'adicionar_lembrete'):
            self.finance_service.adicionar_lembrete(self.usuario_atual, conta, data)
        else:
            if not hasattr(self.usuario_atual, 'lembretes'):
                self.usuario_atual.lembretes = []
            self.usuario_atual.lembretes.append({"conta": conta, "data": data})
            self.auth_service.repo.salvar_usuario(self.usuario_atual)
            
        messagebox.showinfo(_.t("sucesso"), _.t("msg_lembrete_add"))
        self.tela_lembretes()

    def tela_perfil(self):
        """
        Apresenta o painel de configurações da conta do usuário.
        Permite a visualização do e-mail (readonly) e edição de documento e senha.
        """
        self.limpar_janela()
        self.desenhar_menu_lateral(_.t("editar_perfil"))
        
        content = ctk.CTkFrame(self.janela, fg_color="transparent")
        content.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(content, text=_.t("config_conta"), font=("Roboto", 24, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", pady=(0, 20))
        
        # Cartão central que contém o formulário
        form_frame = ctk.CTkFrame(content, width=400, height=450, fg_color=self.CARD_BG)
        form_frame.pack(anchor="w", pady=10, fill="y")
        form_frame.pack_propagate(False)
        
        # Campo de E-mail (Somente leitura - não permite alteração pois é chave única)
        ctk.CTkLabel(form_frame, text=_.t("lbl_email"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(20, 5))
        entry_email = ctk.CTkEntry(form_frame, width=350)
        entry_email.insert(0, self.usuario_atual.email)
        entry_email.configure(state="disabled") # Trava a edição do campo
        entry_email.pack(padx=20)
        
        # Campo de Documento (CPF/CNPJ)
        ctk.CTkLabel(form_frame, text=_.t("lbl_doc"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_perfil_doc = ctk.CTkEntry(form_frame, width=350)
        doc_atual = getattr(self.usuario_atual, 'documento', '') # Busca o documento salvo ou retorna vazio
        self.entry_perfil_doc.insert(0, doc_atual)
        self.entry_perfil_doc.pack(padx=20)
        
        # Campo de edição de Senha
        ctk.CTkLabel(form_frame, text=_.t("lbl_nova_senha"), font=("Roboto", 12, "bold"), text_color=self.TEXT_MAIN).pack(anchor="w", padx=20, pady=(15, 5))
        
        # Inicia preenchido com a senha atual, porém mascarada por '*'
        self.entry_perfil_senha = ctk.CTkEntry(form_frame, width=350, show="*")
        self.entry_perfil_senha.insert(0, self.usuario_atual.senha)
        self.entry_perfil_senha.pack(padx=20)
        
        # --- REQUISITO ENH001: Checkbox de Mascaramento Dinâmico de Senha ---
        # Caixa de seleção para habilitar/desabilitar a visualização dos caracteres da senha
        self.chk_mostrar_senha = ctk.CTkCheckBox(
            form_frame, 
            text=_.t("mostrar_senha", "Mostrar senha"),
            font=("Roboto", 11),
            checkbox_width=16,
            checkbox_height=16,
            command=self.toggle_mostrar_senha_perfil # Ação disparada ao clicar
        )
        self.chk_mostrar_senha.pack(anchor="w", padx=20, pady=(10, 0))
        
        # Botão final para salvar as alterações do formulário
        btn_salvar = ctk.CTkButton(form_frame, text=_.t("btn_salvar_perfil"), command=self.salvar_perfil_gui)
        btn_salvar.pack(pady=35)

    def toggle_mostrar_senha_perfil(self):
        """
        Alterna a visibilidade dos caracteres no campo de edição de senha da tela de perfil.
        Verifica o estado da caixa de seleção (0 ou 1) para determinar a máscara.
        """
        # Se a caixa estiver marcada (1), remove o caractere de máscara
        if self.chk_mostrar_senha.get() == 1:
            self.entry_perfil_senha.configure(show="")
        # Caso desmarcada (0), restaura a máscara com asteriscos
        else:
            self.entry_perfil_senha.configure(show="*")

    def salvar_perfil_gui(self):
        """
        Processa as modificações da tela de perfil.
        Contém regras de negócio de segurança, como validação de branco e 
        verificação do histórico para não permitir reutilização de senhas recentes.
        """
        novo_doc = self.entry_perfil_doc.get().strip()
        nova_senha = self.entry_perfil_senha.get().strip()
        
        # 1. Segurança primária: Impede a definição de senhas vazias
        if not nova_senha:
            return messagebox.showwarning(_.t("aviso"), _.t("msg_senha_branco"))
            
        # --- LÓGICA DE HISTÓRICO DE SENHAS ---
        # Inicializa o controle de histórico de senhas caso o usuário (antigo) não possua
        if not hasattr(self.usuario_atual, 'historico_senhas'):
            self.usuario_atual.historico_senhas = []

        # 2. Avalia se o usuário tentou, de fato, alterar a senha atual
        if nova_senha != self.usuario_atual.senha:
            
            # 3. Regra de Segurança: Verifica se a nova senha já consta no banco de senhas antigas
            if nova_senha in self.usuario_atual.historico_senhas:
                # Bloqueia a ação e alerta o usuário
                return messagebox.showwarning(
                    _.t("aviso_seguranca", "Aviso de Segurança"), 
                    _.t("msg_senha_repetida", "Você não pode reutilizar uma senha antiga por motivos de segurança. Escolha uma senha diferente.")
                )
            
            # Se a nova senha for válida, guardamos a senha ATUAL no histórico antes de sobrescrevê-la
            self.usuario_atual.historico_senhas.append(self.usuario_atual.senha)
            
            # Manutenção do Histórico: Limita o array a guardar apenas as últimas 5 senhas
            # Isso evita que o objeto do usuário cresça excessivamente ao longo do tempo (economia de memória)
            if len(self.usuario_atual.historico_senhas) > 5:
                self.usuario_atual.historico_senhas.pop(0) # Remove a senha mais antiga da lista

        # Atualiza os atributos de documento e senha no objeto em tempo de execução
        self.usuario_atual.documento = novo_doc
        self.usuario_atual.senha = nova_senha
        
        # Submete a gravação no repositório de dados
        self.auth_service.repo.salvar_usuario(self.usuario_atual)
        
        # Fornece o feedback final de sucesso para o usuário
        messagebox.showinfo(_.t("sucesso"), _.t("msg_perfil_ok"))