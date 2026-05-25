#src/goals.py

from src.utils.visual import exibir_cabecalho, BOLD, GREEN, RED, YELLOW, CYAN, WHITE, RESET

# Este módulo permite ao usuário definir objetivos financeiros de curto, médio
# e longo prazo, utilizando estruturas de dicionários para organizar os dados.
def gerenciar_metas(metas):
    """
    Interface de gerenciamento de objetivos financeiros.
    
    Args:
        metas (list): Lista de dicionários contendo 'objetivo' e 'valor'.
    """
    while True:
        # --- RENDERIZAÇÃO DA ABA DE METAS ---
        exibir_cabecalho("Academia Easy Finance - Gerenciamento de Metas")
        print(f"\n{BOLD}1 - ➕ Criar Nova Meta {RESET}")
        print(f"{BOLD}2 - 📋 Ver Minhas Metas{RESET}")
        print(f"{BOLD}0 - ⬅️ Voltar{RESET}")

        escolha = input(f"\n{BOLD}Escolha uma opção: {RESET}")

        # --- FLUXO DE CRIAÇÃO ---
        if escolha == "1":
            nome = input("Qual o seu Objetivo? (ex: Comprar um carro, Fazer uma viagem): ") .strip()
            valor = input("Valor necessário (R$): ") .replace(",", ".").strip() # Permite que o usuário use vírgula como separador decimal
            try:
                valor = float(valor) # Converte o valor para float para garantir que seja numérico
            except ValueError:
                print("❌ Valor inválido! Por favor, digite apenas números.")
                continue
            # Os dados são encapsulados em um dicionário antes de serem inseridos na lista.
            # Isso mantém a integridade dos dados para a persistência em arquivo posterior.
            metas.append({'objetivo': nome, 'valor': valor})
            print(f"{GREEN}✅ Meta '{nome}' guardada com sucesso!{RESET}")
        
        # --- FLUXO DE EXIBIÇÃO ---
        elif escolha == "2":
            print("\n--- MINHAS METAS ---")
            # Validação: verifica se a lista está vazia antes de tentar iterar
            if not metas:
                print("📭 Nenhuma meta cadastrada ainda.")
            else:
                # O uso de enumerate(metas, 1) permite criar uma lista numerada
                # automaticamente para o usuário final a partir do índice 1.
                for i, m in enumerate(metas, 1):
                    # Verificação defensiva: garante que o item atual é um dicionário
                    # para evitar erros de acesso a chaves inexistentes.
                    if isinstance(m, dict):
                        print(f"{i}. {m['objetivo']} - R$ {m['valor']}")
                    else:
                        # Ignora registros corrompidos ou em formatos antigos (legacy data)
                        continue
            input("\nPressione Enter para continuar...")

        elif escolha == "0":
            # Retorno de controle para o módulo chamador (menu anterior)
            break
