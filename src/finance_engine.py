# src/finance_engine.py

# src/finance_engine.py

def exibir_menu_financas():
    print("\n--- REGISTRO FINANCEIRO ---")
    print("1 - Registrar Entrada (Salário, Vendas, etc.)")
    print("2 - Registrar Saída (Aluguel, Contas, etc.)")
    print("0 - Voltar")
    
    escolha = input("Escolha: ")
    
    if escolha == "1":
        valor = float(input("Digite o valor da entrada: "))
        descricao = input("Descrição da entrada: ")
        print(f"✅ R$ {valor} registrado como entrada!")
        # Futuramente, salvaremos isso em uma lista ou CSV
        
    elif escolha == "2":
        valor = float(input("Digite o valor da saída: "))
        descricao = input("Descrição da saída: ")
        print(f"✅ R$ {valor} registrado como saída!")

        # src/finance_engine.py

def registrar_transacao():
    while True:
        print("\n" + "-"*10 + " REGISTRAR FINANÇAS " + "-"*10)
        print("1 - Adicionar Entrada (+)")
        print("2 - Adicionar Saída (-)")
        print("0 - Voltar")
        
        escolha = input("Opção: ")
        if escolha == "1":
            valor = input("Valor da Entrada: R$ ")
            print(f"✅ Receita de R$ {valor} registrada!")
        elif escolha == "2":
            valor = input("Valor da Saída: R$ ")
            print(f"✅ Despesa de R$ {valor} registrada!")
        elif escolha == "0":
            break

def exibir_diagnostico():
    while True:
        print("\n" + "*"*10 + " DIAGNÓSTICO FINANCEIRO " + "*"*10)
        print("1 - Gerar Comparativo Semanal (RF007)")
        print("0 - Voltar")

        escolha = input("Opção: ")
        if escolha == "1":
            print("\n[Lógica de Comparação rodando...]")
            # Aqui você usará aquela lógica de taxa % que fizemos antes
        elif escolha == "0":
            break

def exibir_alertas():
    while True:
        print("\n" + "!"*10 + " ALERTAS DE VENCIMENTO " + "!"*10)
        print("1 - Ver contas que vencem hoje")
        print("0 - Voltar")

        if input("Opção: ") == "0":
            break

# src/finance_engine.py

def exibir_diagnostico(historico_semanal, entradas, saidas, meses_reserva):
    while True:
        print("\n" + "="*10 + " DIAGNÓSTICO FINANCEIRO (RF007) " + "="*10)
        print("1 - Gerar Diagnóstico Atual")
        print("0 - Voltar ao Menu Principal")
        print("="*42)
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            # --- LÓGICA DE DIAGNÓSTICO ---
            if len(historico_semanal) < 2:
                print("\n[!] Sistema: Coletando dados para seu diagnóstico... (Precisas de pelo menos 2 semanas)")
            
            elif entradas == 1 and saidas == 0:
                print("\n[!] Sistema: Dados insuficientes para diagnóstico seguro. Continue registrando!")
            
            else:
                semana_atual = historico_semanal[-1]
                semana_anterior = historico_semanal[-2]
                
                if semana_anterior == 0:
                    print("\n[!] Sistema: Semana anterior sem registro, impossível comparar.")
                else:
                    taxa = ((semana_atual - semana_anterior) / semana_anterior) * 100
                    
                    if taxa > 2:
                        print(f"\n✅ RESULTADO: Taxa de +{taxa:.1f}%. Estás no caminho certo, parabéns!")
                    elif -2 <= taxa <= 2:
                        print(f"\n⚖️ RESULTADO: Taxa de {taxa:.1f}%. Operação estabilizada. Hora de buscar novos clientes?")
                    elif semana_atual < 0:
                        if meses_reserva >= 6:
                            print("\n⚠️ RESULTADO: Semana de caixa negativo, mas as tuas reservas garantem a operação.")
                        else:
                            print(f"\n🚨 CUIDADO: Taxa de {taxa:.1f}%. Risco de falência!")
                    else:
                        print(f"\n⚠️ ATENÇÃO: Taxa de {taxa:.1f}%. O lucro diminuiu, mas ainda não é crítico.")

        elif escolha == "0":
            print("Saindo do Diagnóstico...")
            break
        else:
            print("⚠️ Opção inválida!")        

# src/finance_engine.py

def gerar_relatorio_mensal(entradas, saidas):
    while True:
        print("\n" + "="*10 + " RELATÓRIO MENSAL (RF008) " + "="*10)
        print("1 - Visualizar Balanço Geral")
        print("0 - Voltar ao Menu Principal")
        print("="*42)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            # Calculando os totais
            total_entradas = sum(entradas)
            total_saidas = sum(saidas)
            saldo_final = total_entradas - total_saidas
            
            print("\n" + "-"*25)
            print(f"Total de Entradas: R$ {total_entradas:.2f}")
            print(f"Total de Saídas:   R$ {total_saidas:.2f}")
            print("-" * 25)
            
            if saldo_final >= 0:
                print(f"SALDO ATUAL: R$ {saldo_final:.2f} ✅")
            else:
                print(f"SALDO ATUAL: R$ {saldo_final:.2f} 🚨 (Cuidado!)")
            print("-" * 25)

        elif opcao == "0":
            print("Saindo dos Relatórios...")
            break
        else:
            print("⚠️ Opção inválida!")