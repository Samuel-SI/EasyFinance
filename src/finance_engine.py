# src/finance_engine.py
from datetime import datetime, timedelta

# src/finance_engine.py

# src/finance_engine.py

def exibir_menu_financas(lista_entradas, lista_saidas):
    """
    Interface para registro de movimentações financeiras.
    Recebe as listas de entradas e saídas para armazenamento em memória.
    """ # <--- Aceita as duas listas
    while True:
        print("\n--- REGISTRO FINANCEIRO ---")
        print("1 - Registrar Entrada (Salário, Vendas, etc.)")
        print("2 - Registrar Saída (Aluguel, Contas, etc.)")
        print("0 - Voltar")

        escolha = input("Escolha: ")

        if escolha == "1":
            # Conversão para float permite cálculos com centavos e evita erros de tipo
            valor = float(input("Digite o valor da entrada: "))
            lista_entradas.append(valor) # SALVA NA LISTA
            print(f"✅ R$ {valor} registrado como entrada!")

        elif escolha == "2":
            valor = float(input("Digite o valor da saída: "))
            lista_saidas.append(valor) # SALVA NA LISTA
            print(f"✅ R$ {valor} registrado como saída!")

        elif escolha == "0":
            break # Volta para o main.py
        # src/finance_engine.py

# No seu arquivo src/finance_engine.py

def registrar_transacao(lista_entradas, lista_saidas):
    """
    Gerencia a inserção de novos valores financeiros no sistema.
    As alterações são feitas diretamente nas listas passadas por referência,
    permitindo que o 'main.py' acesse os dados atualizados.
    """ 
    while True:
        print("\n" + "-"*10 + " REGISTRAR FINANÇAS " + "-"*10)
        print("1 - Adicionar Entrada (+)")
        print("2 - Adicionar Saída (-)")
        print("0 - Voltar")

        escolha = input("Opção: ")
        
        if escolha == "1":
            # O tratamento como float é essencial para suportar valores decimais (ex: 50.50)
            valor = float(input("Valor da Entrada: R$ ")) 
            lista_entradas.append(valor) # Adiciona o novo valor ao final da lista de receitas
            print(f"✅ Receita de R$ {valor} registrada!")
            
        elif escolha == "2":
            valor = float(input("Valor da Saída: R$ "))
            lista_saidas.append(valor) # Adiciona o novo valor ao final da lista de despesas
            print(f"✅ Despesa de R$ {valor} registrada!")
            
        elif escolha == "0":
            # Retorna ao fluxo principal sem encerrar o programa
            break


# src/finance_engine.py

from datetime import datetime

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
                    # Trava de segurança para garantir que é um dicionário
                    if isinstance(item, dict):
                        # Transforma o texto da data em uma data real para o Python calcular
                        data_venc = datetime.strptime(item['data'], "%d/%m/%Y")
                        diferenca = data_venc - hoje
                        dias_restantes = diferenca.days + 1

                        # Lógica das cores e dias dinâmicos
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
                # Valida se a data foi digitada no formato certo
                datetime.strptime(data_str, "%d/%m/%Y")
                # GUARDA COMO DICIONÁRIO (O segredo para não dar erro)
                lembretes.append({'conta': conta, 'data': data_str})
                print(f"✅ Lembrete para '{conta}' criado com sucesso!")
            except ValueError:
                print("⚠️ Erro: Use o formato DD/MM/AAAA (Ex: 30/04/2026)")

        elif escolha == "0":
            break
# src/finance_engine.py

def exibir_diagnostico(historico_semanal, entradas, saidas, meses_reserva):
    """
    Analisa a saúde financeira comparando o desempenho entre períodos.
    Utiliza a fórmula de variação percentual: ((V_atual - V_anterior) / V_anterior) * 100
    """
    while True:
        print("\n" + "="*10 + " DIAGNÓSTICO FINANCEIRO (RF007) " + "="*10)
        print("1 - Gerar Diagnóstico Atual")
        print("0 - Voltar ao Menu Principal")
        print("="*42)
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            # Verificação de segurança: evita erro de divisão por zero ou dados insuficientes
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
                    # Cálculo da taxa de crescimento/queda
                    taxa = ((semana_atual - semana_anterior) / semana_anterior) * 100
                    
                    # Interpretação dos resultados (Regras de Negócio)
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
    """
    Gera um balanço simplificado somando todas as entradas e saídas.
    Informa o saldo final e aplica alertas visuais (Emoji) conforme o resultado.
    """
    while True:
        print("\n" + "="*10 + " RELATÓRIO MENSAL (RF008) " + "="*10)
        print("1 - Visualizar Balanço Geral")
        print("0 - Voltar ao Menu Principal")
        print("="*42)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            # A função sum() é utilizada para processar as listas de valores floats
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