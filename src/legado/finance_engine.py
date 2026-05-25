#src/finance_engine.py
from datetime import datetime
from src.utils.visual import (
    exibir_cabecalho, BOLD, GREEN, RED, RESET, 
    formatar_moeda, YELLOW, CYAN, WHITE
)

def registrar_transacao(entradas, saidas):
    """
    Gerencia a inserção de novos valores financeiros no sistema.
    As alterações são feitas diretamente nas listas passadas por referência.
    """ 
    while True:
        exibir_cabecalho("REGISTRAR FINANÇAS")
        print(f"{GREEN}1 -{RESET} Adicionar Entrada (+)")
        print(f"{RED}2 -{RESET} Adicionar Saída (-)")
        print(f"{BOLD}0 -{RESET} Voltar")

        escolha = input(f"\n{BOLD}Opção: {RESET}")

        if escolha == "1":
            try:
                # Conversão de tipo para float garante precisão decimal monetária
                valor = float(input("Valor da Entrada: R$ ")) 
                entradas.append(valor)
                print(f"{GREEN}✅ Receita de R$ {formatar_moeda(valor)} registrada!{RESET}")
            except ValueError:
                # Tratamento de erro caso o usuário digite letras ou símbolos
                print(f"{RED}⚠️ Erro: Digite um valor numérico válido.{RESET}")

        elif escolha == "2":
            try:
                valor = float(input("Valor da Saída: R$ "))
                saidas.append(valor)
                print(f"{RED}✅ Despesa de R$ {formatar_moeda(valor)} registrada!{RESET}")
            except ValueError:
                print(f"{RED}⚠️ Erro: Digite um valor numérico válido.{RESET}")

        elif escolha == "0":
            break

def exibir_alertas(lembretes):
    while True:
        exibir_cabecalho("GESTÃO DE VENCIMENTOS")
        print(f"{CYAN}1 -{RESET} Visualizar Lembretes (Urgência)")
        print(f"{CYAN}2 -{RESET} Criar Novo Lembrete de Pagamento")
        print(f"{BOLD}0 -{RESET} Voltar")

        escolha = input(f"\n{BOLD}Escolha: {RESET}")

        if escolha == "1":
            print("\n--- STATUS DE PAGAMENTOS ---")
            if not lembretes:
                print(f"{GREEN}✅ Tudo em dia! Nenhum lembrete cadastrado.{RESET}")
            else:
                hoje = datetime.now()
                for item in lembretes:
                    if isinstance(item, dict):
                        # Conversão da string (DD/MM/AAAA) para objeto datetime
                        # para permitir operações aritméticas entre datas.
                        data_venc = datetime.strptime(item['data'], "%d/%m/%Y")
                        diferenca = data_venc - hoje
                        # Ajuste do delta de dias para considerar o dia atual
                        dias_restantes = diferenca.days + 1
                        
                        # Lógica de Classificação de Urgência (Sinalização visual)
                        if dias_restantes > 10:
                            status = f"{GREEN}🟢 [LONGO PRAZO]{RESET}"
                        elif 3 < dias_restantes <= 10:
                            status = f"{GREEN}🟢 [SEM URGÊNCIA - {dias_restantes} DIAS]{RESET}"
                        elif 1 < dias_restantes <= 3:
                            status = f"{YELLOW}🟡 [ATENÇÃO - {dias_restantes} DIAS]{RESET}"
                        elif 0 <= dias_restantes <= 1:
                            status = f"{RED}🔴 [ALERTA MÁXIMO - VENCE EM 24H]{RESET}"
                        else:
                            status = f"{WHITE}⚪ [VENCIDO HÁ {abs(dias_restantes)} DIAS]{RESET}"

                        print(f"{status} {BOLD}{item['conta']}{RESET} | Vencimento: {item['data']}")
            input(f"\n{BOLD}Pressione Enter para continuar...{RESET}")

        elif escolha == "2":
            conta = input("Nome da conta: ")
            data_str = input("Vencimento (DD/MM/AAAA): ")
            try:
                # Validação de formato de data antes de inserir na lista
                datetime.strptime(data_str, "%d/%m/%Y")
                lembretes.append({'conta': conta, 'data': data_str})
                print(f"{GREEN}✅ Lembrete para '{conta}' criado com sucesso!{RESET}")
            except ValueError:
                print(f"{RED}⚠️ Erro: Use o formato DD/MM/AAAA.{RESET}")
                input(f"\n{BOLD}Pressione Enter para continuar...{RESET}")

        elif escolha == "0":
            break

def exibir_diagnostico(historico_semanal, entradas, saidas, meses_reserva):
    """
    Analisa a saúde financeira comparando o desempenho entre períodos.
    Utiliza a fórmula de variação percentual: ((V_atual - V_anterior) / V_anterior) * 100
    """
    while True:
        exibir_cabecalho("DIAGNÓSTICO FINANCEIRO")
        print(f"{GREEN}1 -{RESET} Gerar Diagnóstico Atual")
        print(f"{RED}0 -{RESET} Voltar")

        escolha = input(f"\n{BOLD}Escolha uma opção: {RESET}")

        if escolha == "1":
            # Requisito mínimo de 2 pontos de dados para comparação
            if len(historico_semanal) < 2:
                print(f"{YELLOW}[!] Sistema: Coletando dados para seu diagnóstico...{RESET}")
            else:
                semana_atual = historico_semanal[-1]
                semana_anterior = historico_semanal[-2]

                if semana_anterior == 0:
                    print(f"{YELLOW}[!] Sistema: Semana anterior sem registro.{RESET}")
                else:
                    # Cálculo matemático da taxa de variação (V_final - V_inicial) / V_inicial
                    taxa = ((semana_atual - semana_anterior) / semana_anterior) * 100
                    if taxa > 2:
                        print(f"\n✅ RESULTADO: Taxa de +{taxa:.1f}%. Sucesso!")
                    elif -2 <= taxa <= 2:
                        print(f"\n⚖️ RESULTADO: Taxa de {taxa:.1f}%. Estável.")
                    else:
                        print(f"\n🚨 CUIDADO: Taxa de {taxa:.1f}%. Risco!")

        elif escolha == "0":
            break

def gerar_relatorio_mensal(entradas, saidas):
    """
    Gera um balanço simplificado somando todas as entradas e saídas.
    Informa o saldo final e aplica alertas visuais (Emoji) conforme o resultado.
    """
    while True:
        exibir_cabecalho("RELATÓRIO MENSAL")
        print(f"{CYAN}1 -{RESET} Visualizar Balanço Geral")
        print(f"{BOLD}0 -{RESET} Voltar")

        opcao = input(f"\n{BOLD}Escolha uma opção: {RESET}")

        if opcao == "1":
            # Utiliza a função built-in sum() para iteração eficiente sobre as listas
            exibir_cabecalho("EXTRATO DETALHADO")
            print(f"{BOLD}{'-'*45}")
            print(f"{'TIPO':<15} | {'VALOR':<25}")
            print(f"{'-'*45}{RESET}")

            # Listando as Entradas
            for e in entradas:
                print(f"{GREEN}{'ENTRADA':<15}{RESET} | {formatar_moeda(e):<25}")
            
            # Listando as Saídas
            for s in saidas:
                print(f"{RED}{'SAÍDA':<15}{RESET} | {formatar_moeda(s):<25}")

            print(f"{BOLD}{'-'*45}{RESET}")


            total_entradas = sum(entradas)
            total_saidas = sum(saidas)
            saldo_final = total_entradas - total_saidas

            print(f"\n{GREEN} Total Entradas: R$ {formatar_moeda(total_entradas)}")
            print(f"{RED}Total Saídas:   R$ {formatar_moeda(total_saidas)}")

            # Condicional de controle visual para o saldo
            cor_saldo = GREEN if saldo_final >= 0 else RED
            emoji = "✅" if saldo_final >= 0 else "🚨"
            
            print(f"{CYAN}SALDO ATUAL:    {cor_saldo}{formatar_moeda(saldo_final)} {emoji}{RESET}")
            input(f"\n{BOLD}Pressione Enter para continuar...{RESET}")

        elif opcao == "0":
            break