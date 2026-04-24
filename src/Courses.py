# src/Courses.py
import webbrowser
def exibir_cursos():
    while True:
        print("\n" + "="*10 + " ABA DE CURSOS (RF010) " + "="*10)
        print("1 - Curso: Educação Financeira Básica")
        print("2 - Curso: Como sair das dívidas")
        print("3 - Curso: Investimentos para Iniciantes")
        print("0 - Voltar ao Menu Principal")
        print("="*43)

        escolha = input("Escolha um curso para ver detalhes: ")

        if escolha == "1":
            print("\n[Detalhes] Aprenda a organizar seu orçamento mensal do zero.")
        elif escolha == "2":
            print("\n[Detalhes] Estratégias para negociar juros e quitar boletos.")
        elif escolha == "3":
            print("\n[Detalhes] O que é Selic, CDB e como começar a investir.")
        elif escolha == "0":
            print("Saindo da Aba de Cursos...")
            break
        else:
            print("⚠️ Opção inválida!")