#src/interface.py
from src.finance_engine import registrar_transacao, exibir_alertas, exibir_diagnostico, gerar_relatorio_mensal
from src.Courses import exibir_cursos
from src.goals import gerenciar_metas
from src.database import salvar_dados, carregar_sessao_usuario, salvar_valores_financeiros

def menu_principal(usuario_logado):
    """
    Exibe o menu de funcionalidades principais após o login.
    Controla o fluxo entre as abas de finanças, cursos, metas e relatórios.
    """
    # Carrega as informações dos arquivos de texto para as listas em memória ao iniciar o programa
    lista_metas, lista_lembretes, valores_entradas, valores_saidas = carregar_sessao_usuario(usuario_logado)

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
            registrar_transacao(valores_entradas, valores_saidas)
            salvar_valores_financeiros(f'entradas_{usuario_logado}.txt', valores_entradas)
            salvar_valores_financeiros(f'saidas_{usuario_logado}.txt', valores_saidas)
            print("💾 Dados gravados com sucesso!")
            
        elif escolha == "2":
            # 1. Chama a função de alertas enviando a lista
            exibir_alertas(lista_lembretes)
            # 2. ASSIM QUE VOLTAR DA FUNÇÃO, SALVA NO ARQUIVO:
            salvar_dados(f'lembretes_{usuario_logado}.txt', lista_lembretes)
            print("💾 Lembretes sincronizados com o banco de dados!")

        elif escolha == "3":
            # O diagnóstico calcula saúde financeira baseada em entradas vs saídas
            # Parâmetros: [Reserva Alvo], Total Entradas, Total Saídas, Meses de Cobertura
            saldo_total = sum(valores_entradas) - sum(valores_saidas)
            historico_real = [1000, saldo_total]
            exibir_diagnostico(historico_real, sum(valores_entradas), sum(valores_saidas), 6)

        elif escolha == "4":
             gerar_relatorio_mensal(valores_entradas, valores_saidas) # Chama a página de relatórios
             
        elif escolha == "5":
           exibir_cursos() # Chama a página de cursos

        elif escolha == "6":
            gerenciar_metas(lista_metas)
            # Menu de metas pessoais com salvamento automático ao sair da aba
            salvar_dados(f'metas_{usuario_logado}.txt', lista_metas)
            print("💾 Metas sincronizadas com o banco de dados!")
            
        elif escolha == "0":
            print("\nSessão encerrada!")
            break 
        else:
            print("\nOpção inválida!")