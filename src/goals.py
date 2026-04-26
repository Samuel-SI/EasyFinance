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
        print("\n" + "-"*15 + " ABA DE METAS " + "-"*15)
        print("1 - Criar Nova Meta")
        print("2 - Ver Minhas Metas")
        print("0 - Voltar")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Objetivo: ")
            valor = input("Valor: ")
            # Os dados são encapsulados em um dicionário antes de serem inseridos na lista.
            # Isso mantém a integridade dos dados para a persistência em arquivo posterior.
            metas.append({'objetivo': nome, 'valor': valor})
            print("✅ Meta guardada!")

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
            break