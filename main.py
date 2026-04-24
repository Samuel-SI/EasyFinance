# main.py
import sys
import os

# Esse comando ajuda o Python a encontrar a pasta 'src' se ele se perder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.validators import realizar_cadastro
from src.finance_engine import exibir_menu_financas, exibir_alertas, exibir_diagnostico, gerar_relatorio_mensal
from src.Courses import exibir_cursos
from src.goals import gerenciar_metas
from src.database import salvar_dados, carregar_dados, salvar_valores_financeiros, carregar_valores_financeiros

# Carregar dados existentes ao iniciar
lista_emails = carregar_dados('emails.txt')
lista_senhas = carregar_dados('senhas.txt')
lista_documentos = carregar_dados('documentos.txt')
valores_entradas = carregar_valores_financeiros('entradas.txt')
valores_saidas = carregar_valores_financeiros('saidas.txt')

def menu_principal():
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
            exibir_menu_financas() # Chama a página de finanças
        elif escolha == "2":
            exibir_alertas() # Chama a página de alertas
        elif escolha == "3":
           exibir_diagnostico() # Chama a página de diagnóstico
        elif escolha == "4":
             gerar_relatorio_mensal() # Chama a página de relatórios
        elif escolha == "5":
           exibir_cursos() # Chama a página de cursos
        elif escolha == "6":
            gerenciar_metas() # Chama a página de metas
        elif escolha == "0":
            print("\nSessão encerrada!")
            break # Sai do menu principal e volta para o menu de Login/Cadastro
        else:
            print("\nOpção inválida!")

def fazer_login():
    print("\n==== TELA DE LOGIN ====")
    if not lista_emails:
        print("⚠️ Nenhum usuário cadastrado.")
        return False
    
    email_login = input("E-mail: ")
    senha_login = input("Senha: ")

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

# --- MENU ---
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
        e, s, d = realizar_cadastro(lista_emails, lista_documentos)
        lista_emails.append(e)
        lista_senhas.append(s)
        lista_documentos.append(d)
        
        # SALVAR NO ARQUIVO AGORA
        salvar_dados('emails.txt', lista_emails)
        salvar_dados('senhas.txt', lista_senhas)
        salvar_dados('documentos.txt', lista_documentos)
        print("✅ Cadastro finalizado!")
        
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")