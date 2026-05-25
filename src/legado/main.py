#main.py
   
import sys
import os

# ==============================================================================
# CONFIGURAÇÃO DE AMBIENTE E PATH
# ==============================================================================
# O código abaixo localiza o diretório 'src' de forma dinâmica, garantindo que
# o Python encontre os módulos internos independentemente de onde o script é executado.

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# --- IMPORTAÇÃO DE MÓDULOS INTERNOS ---
from src.auth import fazer_login
from src.utils.validators import realizar_cadastro
from src.interface import menu_principal
from src.database import obter_listas_autenticacao, cadastrar_novo_usuario, inicializar_banco
from src.security import verificar_2fa
from src.utils.visual import exibir_cabecalho, BOLD, RED, GREEN, BLUE, RESET, limpar_tela
  
# --- INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
# Carrega as informações dos arquivos de texto para as listas em memória ao iniciar o programa
inicializar_banco()

lista_emails, lista_senhas, lista_documentos = obter_listas_autenticacao()

# --- LOOP PRINCIPAL DO SISTEMA ---
while True:
    limpar_tela()  # Limpa a tela a cada iteração para melhor UX
    exibir_cabecalho("=== EASY FINANCE ===")
    print(f"{GREEN}1 - Login{RESET}")
    print(f"{BLUE}2 - Cadastro{RESET}")
    print(f"{RED}0 - Sair{RESET}")

    opcao = input(f"\n{BOLD}Escolha uma opção: {RESET}")

    # --- FLUXO DE AUTENTICAÇÃO (LOGIN) ---
    if opcao == "1":
        usuario_logado = fazer_login()
        if usuario_logado:
            # Camada adicional de segurança: Autenticação de Dois Fatores
            if verificar_2fa(usuario_logado):
               menu_principal(usuario_logado)
    
    elif opcao == "2":
        # Processo de cadastro: recebe dados, armazena em listas e persiste em arquivo
        e, s, d = realizar_cadastro(lista_emails, lista_documentos)
        lista_emails.append(e)
        lista_senhas.append(s)
        lista_documentos.append(d)

        cadastrar_novo_usuario(e, s, d)


        print(f"✅ Cadastro de {e} realizado com sucesso!")
        input("Pressione Enter para continuar...")

    elif opcao == "0":
        print(f"\n{BLUE}Obrigado por usar o Easy Finance... Até logo!{RESET}")
        break
    else:
        input(f"\n{BOLD}⚠️ Opção inválida! Pressione Enter para tentar novamente...{RESET}")

