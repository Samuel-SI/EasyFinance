# src/goals.py

# src/goals.py

def gerenciar_metas():
    while True:
        print("\n" + "-"*10 + " ABA DE METAS " + "-"*10)
        print("1 - Criar Nova Meta")
        print("2 - Ver Minhas Metas")
        print("0 - Voltar ao Menu Principal")
        print("-"*34)
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\n--- CRIAR NOVA META ---")
            nome_meta = input("Qual o seu objetivo? (ex: Viagem): ")
            valor_meta = input("Quanto precisa poupar? R$ ")
            print(f"✅ Meta '{nome_meta}' registada!")
            
        elif escolha == "2":
            print("\n--- MINHAS METAS ---")
            print("Ainda não tens metas guardadas.") # Futuramente lerás do arquivo
            
        elif escolha == "0":
            print("A sair da Aba de Metas...")
            break # Este 'break' faz o programa sair do loop e voltar para o main.py
            
        else:
            print("⚠️ Opção inválida! Tenta novamente.")