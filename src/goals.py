def gerenciar_metas(metas):
    while True:
        print("\n" + "-"*15 + " ABA DE METAS " + "-"*15)
        print("1 - Criar Nova Meta")
        print("2 - Ver Minhas Metas")
        print("0 - Voltar")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            nome = input("Objetivo: ")
            valor = input("Valor: ")
            # Salva como dicionário para manter o padrão do sistema
            metas.append({'objetivo': nome, 'valor': valor})
            print("✅ Meta guardada!")

        elif escolha == "2":
            print("\n--- MINHAS METAS ---")
            if not metas:
                print("📭 Nenhuma meta cadastrada ainda.")
            else:
                for i, m in enumerate(metas, 1):
                    # AQUI ESTÁ A ALTERAÇÃO:
                    # Como 'm' já é um dicionário, acessamos direto pelas chaves
                    if isinstance(m, dict):
                        print(f"{i}. {m['objetivo']} - R$ {m['valor']}")
                    else:
                        # Caso ainda exista algum texto antigo no arquivo .txt
                        continue
            input("\nPressione Enter para continuar...")

        elif escolha == "0":
            break