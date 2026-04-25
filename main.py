import sys
import os

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Adiciona o diretório 'src' ao path do sistema para permitir a importação de módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# --- IMPORTAÇÃO DE MÓDULOS INTERNOS ---
from src.validators import realizar_cadastro
from src.finance_engine import exibir_menu_financas, exibir_alertas, exibir_diagnostico, gerar_relatorio_mensal
from src.Courses import exibir_cursos
from src.goals import gerenciar_metas
from src.database import salvar_dados, carregar_dados, carregar_valores_financeiros, salvar_valores_financeiros, carregar_valores_financeiros

# --- INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
# Carrega as informações dos arquivos de texto para as listas em memória ao iniciar o programa
lista_emails = carregar_dados('emails.txt')
lista_senhas = carregar_dados('senhas.txt')
lista_documentos = carregar_dados('documentos.txt')
valores_entradas = carregar_valores_financeiros('entradas.txt')
valores_saidas = carregar_valores_financeiros('saidas.txt')
lista_metas = carregar_dados('metas.txt')
lista_lembretes = carregar_dados('lembretes.txt')

def menu_principal():
    """
    Exibe o menu de funcionalidades principais após o login.
    Controla o fluxo entre as abas de finanças, cursos, metas e relatórios.
    """
    while True:
        print("\n" + "="*30)
        print("      EASY FINANCE - HOME")
        print("="*30)
        print("1 - Registrar Entrada/Saída")
        print("2 - Alertas de Vencimento")
        print("3 - Diagnóstico Financeiro")
        print("4 - Relatórios Mensais")
        print("5 - Aba de Cursos")
        print("6 - Aba de Metas")
        print("0 - Encerrar Sessão (Logout)")
        print("="*30)

        escolha = input("Escolha uma opção: ")

        
        if escolha == "1":
            # Gerencia entradas e saídas e sincroniza as alterações no banco de dados
            exibir_menu_financas(valores_entradas, valores_saidas)
            salvar_valores_financeiros('entradas.txt', valores_entradas)
            salvar_valores_financeiros('saidas.txt', valores_saidas)
            print("💾 Dados gravados com sucesso!")
        elif escolha == "2":
            # 1. Chama a função de alertas enviando a lista
            exibir_alertas(lista_lembretes)
            
            # 2. ASSIM QUE VOLTAR DA FUNÇÃO, SALVA NO ARQUIVO:
            salvar_dados('lembretes.txt', lista_lembretes)
            print("💾 Lembretes sincronizados com o banco de dados!")
        
        elif escolha == "3":
            # Gera análise baseada no histórico e reserva de emergência
            exibir_diagnostico([1000, 1100], sum(valores_entradas), sum(valores_saidas), 6)
        
        elif escolha == "4":
             gerar_relatorio_mensal(valores_entradas, valores_saidas) # Chama a página de relatórios
        elif escolha == "5":
           exibir_cursos() # Chama a página de cursos
        
        elif escolha == "6":
            gerenciar_metas(lista_metas)
            
            # Menu de metas pessoais com salvamento automático ao sair da aba
            salvar_dados('metas.txt', lista_metas)
            print("💾 Metas sincronizadas com o banco de dados!")
        elif escolha == "0":
            print("\nSessão encerrada!")
            break # Sai do menu principal e volta para o menu de Login/Cadastro
        else:
            print("\nOpção inválida!")

def fazer_login():
    """
    Realiza a autenticação do usuário.
    Verifica se o e-mail existe e se a senha corresponde ao índice do e-mail.
    Retorna True para sucesso e False para falha.
    """
    print("\n==== TELA DE LOGIN ====")
    if not lista_emails:
        print("⚠️ Nenhum usuário cadastrado.")
        return False
    
    email_login = input("E-mail: ")
    senha_login = input("Senha: ")

    # Validação de credenciais através de busca por índice
    if email_login in lista_emails:
        indice = lista_emails.index(email_login)
        if senha_login == lista_senhas[indice]:
            print(f"✅ Login realizado com sucesso!")
            return True
        else:
            print("❌ Senha incorreta!")
    else:
        print("❌ Usuário não encontrado!")
    return False

# --- LOOP PRINCIPAL DO SISTEMA ---
while True:
    print("\n=== EASY FINANCE ===")
    print("1 - Login")
    print("2 - Cadastro")
    print("0 - Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        if fazer_login():
            menu_principal()
    elif opcao == "2":
        # Processo de cadastro: recebe dados, armazena em listas e persiste em arquivo
        e, s, d = realizar_cadastro(lista_emails, lista_documentos)
        lista_emails.append(e)
        lista_senhas.append(s)
        lista_documentos.append(d)
        
        # SALVAR NO ARQUIVO AGORA
        salvar_dados('emails.txt', lista_emails)
        salvar_dados('senhas.txt', lista_senhas)
        salvar_dados('documentos.txt', lista_documentos)
        salvar_dados('metas.txt', lista_metas)
        print("✅ Cadastro finalizado!")
        
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")