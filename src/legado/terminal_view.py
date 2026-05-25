import webbrowser
from src.services.auth_service import AuthService
from src.services.finance_service import FinanceService
from src.models.usuario import Usuario
import src.utils.visual as vis

class TerminalView:
    """Gerencia todas as telas, menus e interações via terminal com o usuário."""
    
    def __init__(self, auth_service: AuthService, finance_service: FinanceService):
        self.auth_service = auth_service
        self.finance_service = finance_service

    def iniciar(self):
        """Ponto de partida da interface."""
        while True:
            vis.exibir_cabecalho("EASYFINANCE - BEM-VINDO")
            print("1. Fazer Login")
            print("2. Criar Conta")
            print("3. Sair")
            print(f"{vis.BLUE}{'='*50}{vis.RESET}")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == '1':
                self.tela_login()
            elif opcao == '2':
                self.tela_cadastro()
            elif opcao == '3':
                print(f"\n{vis.GREEN}Obrigado por usar o EasyFinance! Até logo.{vis.RESET}")
                break
            else:
                print(f"\n{vis.RED}Opção inválida! Pressione Enter para tentar novamente.{vis.RESET}")
                input()

    def tela_cadastro(self):
        vis.exibir_cabecalho("NOVO CADASTRO")
        email = input("Digite seu e-mail: ")
        documento = input("Digite seu CPF ou CNPJ: ")
        senha = input("Crie uma senha: ")
        
        sucesso, mensagem = self.auth_service.cadastrar_usuario(email, documento, senha)
        
        cor = vis.GREEN if sucesso else vis.RED
        print(f"\n{cor}{mensagem}{vis.RESET}")
        input("\nPressione Enter para continuar...")

    def tela_login(self):
        vis.exibir_cabecalho("LOGIN")
        email = input("E-mail: ")
        senha = input("Senha: ")
        
        sucesso, resultado = self.auth_service.realizar_login(email, senha)
        
        if sucesso:
            usuario_logado = resultado
            print(f"\nEnviando código de segurança para {usuario_logado.email}")
            codigo_gerado = self.auth_service.enviar_2fa_email(usuario_logado.email)

            if not codigo_gerado:
                print(f"\n{vis.RED}Não foi possível enviar o código de segurança. Verifique a sua conexão com a internet e tente novamente{vis.RESET}")
                input("\nPressione Enter para voltar...")
                return
            vis.exibir_cabecalho("AUTENTIFICAÇÃO DE DOIS FATORES(2FA)")

            tentativas = 3
            while tentativas > 0:
                codigo_inserido = input("\nDigite o código de segurança enviado para o seu e-mail: ").strip()

                if codigo_inserido == codigo_gerado:
                    print(f"\n{vis.GREEN}✅ Código correto! Acesso concedido.{vis.RESET}")
                    input("\nPressione Enter para acessar o painel...")
                    self.menu_principal(usuario_logado)
                    return
                else:
                    tentativas -= 1
                    print(f"{vis.RED}❌ Código incorreto! Você tem mais {tentativas} tentativas.{vis.RESET}")
            print(f"\n{vis.RED}🚨 Acesso Bloqueado: Muitas tentativas falhas.{vis.RESET} ")
            input("\nPressione Enter para voltar ao menu...")
        else:
            print(f"\n{vis.RED}{resultado}{vis.RESET}")
            input("\nPressione Enter para voltar...")

    def menu_principal(self, usuario: Usuario):
        """Menu interno após o login com sucesso."""
        while True:
            vis.exibir_cabecalho(f"PAINEL DE CONTROLE - {usuario.nivel.upper()}")
            saldo = usuario.calcular_saldo()
            
            print(f"Usuário: {usuario.email}")
            print(f"Saldo Atual: {vis.formatar_moeda(saldo)}")
            print(f"Pontos B2B: {usuario.pontos} | Cursos Concluídos: {usuario.cursos_concluidos}")
            print(f"{vis.BLUE}{'='*50}{vis.RESET}")
            
            print("1. Adicionar Transação (Entrada/Saída)")
            print("2. Ver Extrato")
            print("3. Adicionar Lembrete de Conta")
            print("4. Adicionar Meta de Negócio")
            print("5. Área de Educação (Assistir Curso)")
            print("6. Fazer Logout")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == '1':
                self.tela_adicionar_transacao(usuario)
            elif opcao == '2':
                self.tela_extrato(usuario)
            elif opcao == '3':
                self.tela_adicionar_lembrete(usuario)
            elif opcao == '4':
                self.tela_adicionar_meta(usuario)
            elif opcao == '5':
                self.tela_educacao(usuario)
            elif opcao == '6':
                break
            else:
                print(f"{vis.RED}Opção inválida!{vis.RESET}")
                input()

    def tela_adicionar_transacao(self, usuario: Usuario):
        vis.exibir_cabecalho("NOVA TRANSAÇÃO")
        tipo = input("Tipo (E para Entrada / S para Saída): ").upper()
        tipo_str = "ENTRADA" if tipo == 'E' else "SAÍDA" if tipo == 'S' else None
        
        if not tipo_str:
            print(f"{vis.RED}Tipo inválido!{vis.RESET}")
            input()
            return
            
        try:
            valor = float(input("Valor (Ex: 150.50): "))
            descricao = input("Descrição: ")
            
            sucesso = self.finance_service.adicionar_transacao(usuario, tipo_str, valor, descricao)
            if sucesso:
                print(f"\n{vis.GREEN}Transação adicionada com sucesso!{vis.RESET}")
            else:
                print(f"\n{vis.RED}Valor inválido.{vis.RESET}")
        except ValueError:
            print(f"\n{vis.RED}Erro: Digite apenas números no valor.{vis.RESET}")
        
        input("\nPressione Enter para voltar...")

    def tela_extrato(self, usuario: Usuario):
        vis.exibir_cabecalho("EXTRATO FINANCEIRO")
        lista_dit = [t.para_dicionario() for t in usuario.transacoes]
        vis.exibir_tabela_financeira(lista_dit)
        input("\nPressione Enter para voltar...")

    def tela_adicionar_lembrete(self, usuario: Usuario):
        vis.exibir_cabecalho("NOVO LEMBRETE")
        conta = input("Nome da conta (Ex: Luz, Internet): ")
        data = input("Data de vencimento (DD/MM/AAAA): ")
        self.finance_service.adicionar_lembrete(usuario, conta, data)
        print(f"\n{vis.GREEN}Lembrete salvo com sucesso!{vis.RESET}")
        input("\nPressione Enter para voltar...")

    def tela_adicionar_meta(self, usuario: Usuario):
        vis.exibir_cabecalho("NOVA META")
        objetivo = input("Qual o objetivo (Ex: Comprar notebook): ")
        try:
            valor = float(input("Qual o valor necessário: "))
            self.finance_service.adicionar_meta(usuario, objetivo, valor)
            print(f"\n{vis.GREEN}Meta registrada! Continue evoluindo.{vis.RESET}")
        except ValueError:
            print(f"\n{vis.RED}Erro: Valor inválido.{vis.RESET}")
        input("\nPressione Enter para voltar...")

    def tela_educacao(self, usuario: Usuario):
        vis.exibir_cabecalho("ÁREA DE EDUCAÇÃO - EASY FINANCE")
        cursos = [
            {"id": "1", "titulo": "Finanças para Iniciantes: Do Zero ao Primeiro Investimento", "canal": "Primo Pobre", "url": "https://www.youtube.com/watch?v=F3a37yG265A"},
            {"id": "2", "titulo": "Como Organizar suas Finanças e Sair das Dívidas", "canal": "Me Poupe!", "url": "https://www.youtube.com/watch?v=A_cQp2ZgBkw"},
            {"id": "3", "titulo": "Como Separar a Conta Física da Jurídica (MEI/Empresas)", "canal": "Sebrae", "url": "https://www.youtube.com/watch?v=H7yV23V4h3Y"},
            {"id": "4", "titulo": "Guia Prático: Como Montar sua Reserva de Emergência", "canal": "Nath Finanças", "url": "https://www.youtube.com/watch?v=UqN69zVn2q0"},
            {"id": "5", "titulo": "Onde Investir 100 Reais Hoje? (Renda Fixa Prática)", "canal": "Gêmeos Investidores", "url": "https://www.youtube.com/watch?v=3IeP9R7oAt8"},
            {"id": "6", "titulo": "Controle de Fluxo de Caixa para Pequenos Negócios", "canal": "Jovens de Negócios", "url": "https://www.youtube.com/watch?v=687pL-C9Zms"},
            {"id": "7", "titulo": "Como Funciona o Tesouro Direto na Prática", "canal": "Você MAIS Rico", "url": "https://www.youtube.com/watch?v=Vl03C8vD84E"},
            {"id": "8", "titulo": "Os 3 Erros Fatais que Quebram Qualquer Empresa", "canal": "Erico Rocha", "url": "https://www.youtube.com/watch?v=I4w3bO_f5y4"},
            {"id": "9", "titulo": "Como Declarar Imposto de Renda Sendo Autônomo/MEI", "canal": "Contabilidade Facilitada", "url": "https://www.youtube.com/watch?v=9_7P86uI0j0"},
            {"id": "10", "titulo": "Psicologia do Dinheiro: Como sua Mente te Deixa Pobre", "canal": "IlustradaMente", "url": "https://www.youtube.com/watch?v=P_D652yT_bY"},
        ]
        print(f"Nível atual: {vis.BOLD}{usuario.ranking}{vis.RESET} | Pontos acumulados: {usuario.pontos}\n")
        print(f"{vis.BOLD}Aulas Práticas Disponíveis (Abrem no YouTube):{vis.RESET}")
        print("-" * 85)
        for c in cursos:
            print(f" [{c['id'].zfill(2)}] {c['titulo'].ljust(58)} | {vis.BLUE}{c['canal']}{vis.RESET}")
        print("-" * 85)
        print(" [00] Voltar ao Menu Anterior")
        
        opcao = input("\nDigite o número do curso que deseja assistir: ").strip()
        opcao_normalizada = str(int(opcao)) if opcao.isdigit() else option

        if opcao_normalizada == 0:
            return
        
        curso_escolhido = next((c for c in cursos if c["id"] == opcao_normalizada), None)

        if curso_escolhido:
            vis.exibir_cabecalho(f"REDIRECIONANDO: {curso_escolhido['titulo'].upper()}")
            print(f"Canal parceiro: {vis.BOLD}{curso_escolhido['canal']}{vis.RESET}")
            print("\nAbrindo o seu navegador de internet...")

            webbrowser.open(curso_escolhido["url"])

            print(f"\n{vis.GREEN}O vídeo foi aberto na sua tela! Aproveito o conteúdo. {vis.RESET}")
            print("-" * 65)
            print(f" Após assistir o vídeo completo, valide abaixo para evoluir seu negócio: ")
            print("[1] Marcar a aula como concluída(Garantir pontuação)")
            print("[2] Sair sem concluir( Apenas assistir )")
            decisao = input("\nO que deseja fazer?").strip()

            if decisao == 1:
                mensagem = self.finance_service.computar_curso_concluido(usuario)
                print(f"{vis.GREEN}✅ {mensagem}{vis.RESET}")
            else:
                print(f"\n{vis.RED}Você não marcou a aula como concluída. Nenhum ponto computado. {vis.RESET}")
        else:
            print(f"\n{vis.RED}Opção inválida!{vis.RESET}")
        
        input("\nPressione Enter para continuar...")