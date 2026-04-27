from datetime import datetime

def registrar_transacao(lista_entradas, lista_saidas):
    """
    Gerencia a inserção de novos valores financeiros no sistema.
    As alterações são feitas diretamente nas listas passadas por referência.
    """ 
    while True:
        print("\n" + "-"*10 + " REGISTRAR FINANÇAS " + "-"*10)
        print("1 - Adicionar Entrada (+)")
        print("2 - Adicionar Saída (-)")
        print("0 - Voltar")

        escolha = input("Opção: ")

        if escolha == "1":
            try:
                valor = float(input("Valor da Entrada: R$ ")) 
                lista_entradas.append(valor)
                print(f"✅ Receita de R$ {valor} registrada!")
            except ValueError:
                print("⚠️ Erro: Digite um valor numérico válido.")

        elif escolha == "2":
            try:
                valor = float(input("Valor da Saída: R$ "))
                lista_saidas.append(valor)
                print(f"✅ Despesa de R$ {valor} registrada!")
            except ValueError:
                print("⚠️ Erro: Digite um valor numérico válido.")

        elif escolha == "0":
            break

def exibir_alertas(lembretes):
    while True:
        print("\n" + "!"*10 + " GESTÃO DE VENCIMENTOS " + "!"*10)
        print("1 - Visualizar Lembretes (Urgência)")
        print("2 - Criar Novo Lembrete de Pagamento")
        print("0 - Voltar")

        escolha = input("Escolha: ")

        if escolha == "1":
            print("\n--- STATUS DE PAGAMENTOS ---")
            if not lembretes:
                print("✅ Tudo em dia! Nenhum lembrete cadastrado.")
            else:
                hoje = datetime.now()
                for item in lembretes:
                    if isinstance(item, dict):
                        data_venc = datetime.strptime(item['data'], "%d/%m/%Y")
                        diferenca = data_venc - hoje
                        dias_restantes = diferenca.days + 1

                        if dias_restantes > 10:
                            status = "🟢 [LONGO PRAZO]"
                        elif 3 < dias_restantes <= 10:
                            status = f"🟢 [SEM URGÊNCIA - {dias_restantes} DIAS]"
                        elif 1 < dias_restantes <= 3:
                            status = f"🟡 [ATENÇÃO - {dias_restantes} DIAS]"
                        elif 0 <= dias_restantes <= 1:
                            status = "🔴 [ALERTA MÁXIMO - VENCE EM 24H]"
                        else:
                            status = f"⚪ [VENCIDO HÁ {abs(dias_restantes)} DIAS]"

                        print(f"{status} {item['conta']} | Vencimento: {item['data']}")
            input("\nPressione Enter para continuar...")

        elif escolha == "2":
            conta = input("Nome da conta: ")
            data_str = input("Vencimento (DD/MM/AAAA): ")
            try:
                datetime.strptime(data_str, "%d/%m/%Y")
                lembretes.append({'conta': conta, 'data': data_str})
                print(f"✅ Lembrete para '{conta}' criado com sucesso!")
            except ValueError:
                print("⚠️ Erro: Use o formato DD/MM/AAAA.")

        elif escolha == "0":
            break

def exibir_diagnostico(historico_semanal, entradas, saidas, meses_reserva):
    """
    Analisa a saúde financeira comparando o desempenho entre períodos.
    Utiliza a fórmula de variação percentual: ((V_atual - V_anterior) / V_anterior) * 100
    """
    while True:
        print("\n" + "="*10 + " DIAGNÓSTICO FINANCEIRO " + "="*10)
        print("1 - Gerar Diagnóstico Atual")
        print("0 - Voltar")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if len(historico_semanal) < 2:
                print("\n[!] Sistema: Coletando dados para seu diagnóstico...")
            else:
                semana_atual = historico_semanal[-1]
                semana_anterior = historico_semanal[-2]

                if semana_anterior == 0:
                    print("\n[!] Sistema: Semana anterior sem registro.")
                else:
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
        print("\n" + "="*10 + " RELATÓRIO MENSAL " + "="*10)
        print("1 - Visualizar Balanço Geral")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            total_entradas = sum(entradas)
            total_saidas = sum(saidas)
            saldo_final = total_entradas - total_saidas

            print(f"\nTotal Entradas: R$ {total_entradas:.2f}")
            print(f"Total Saídas:   R$ {total_saidas:.2f}")
            if saldo_final >= 0:
                print(f"SALDO ATUAL: R$ {saldo_final:.2f} ✅")
            else:
                print(f"SALDO ATUAL: R$ {saldo_final:.2f} 🚨")

        elif opcao == "0":
            break