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
from src.validators import realizar_cadastro
from src.interface import menu_principal
from src.database import salvar_dados, carregar_dados
from src.security import verificar_2fa 
  
# --- INICIALIZAÇÃO DE DADOS (PERSISTÊNCIA) ---
# Carrega as informações dos arquivos de texto para as listas em memória ao iniciar o programa
lista_emails = carregar_dados('emails.txt')
lista_senhas = carregar_dados('senhas.txt')
lista_documentos = carregar_dados('documentos.txt')

# --- LOOP PRINCIPAL DO SISTEMA ---
while True:
    print("\n=== EASY FINANCE ===")
    print("1 - Login")
    print("2 - Cadastro")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        usuario_logado = fazer_login(lista_emails, lista_senhas)
        if usuario_logado:
            if verificar_2fa(usuario_logado):
               menu_principal(usuario_logado)
    elif opcao == "2":
        # Processo de cadastro: recebe dados, armazena em listas e persiste em arquivo
        e, s, d = realizar_cadastro(lista_emails, lista_documentos)
        lista_emails.append(e)
        lista_senhas.append(s)
        lista_documentos.append(d)

        # SALVAR NO ARQUIVO 
        salvar_dados('emails.txt', lista_emails)
        salvar_dados('senhas.txt', lista_senhas)
        salvar_dados('documentos.txt', lista_documentos)
        print("✅ Cadastro finalizado!")

    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida!")