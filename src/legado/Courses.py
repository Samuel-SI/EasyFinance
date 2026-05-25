# src/Courses.py
from src.utils.visual import (
    exibir_cabecalho, BOLD, GREEN, RED, YELLOW, BLUE, CYAN, WHITE, RESET, 
)



def exibir_cursos():
    """
    Exibe um menu interativo com recomendações de cursos e materiais educativos.
    O objetivo é fornecer recursos externos para a educação financeira do usuário.
    """
    cursos = [{"tema": "Organização para Iniciantes", "autor": "Nath Finanças", "link": "https://www.youtube.com/watch?v=zV_zE02UshE", "dica": "Regra dos 50-30-20."},
        {"tema": "Como sair das dívidas", "autor": "Nath Arcuri", "link": "https://www.youtube.com/watch?v=7p_GZfOAsFw", "dica": "Priorize juros altos."},
        {"tema": "Selic e Investimentos Básicos", "autor": "Primo Pobre", "link": "https://www.youtube.com/watch?v=3mY_2S4V2Is", "dica": "Reserva de emergência primeiro."},
        {"tema": "Mentalidade de Riqueza", "autor": "Tiago Nigro", "link": "https://www.youtube.com/watch?v=689N7pI9mGk", "dica": "Pague-se primeiro."},
        {"tema": "Bolsa de Valores do Zero", "autor": "Bea Aguillar", "link": "https://www.youtube.com/watch?v=mY2C6fJzQ0M", "dica": "Pense no longo prazo."},
        {"tema": "Economia Doméstica", "autor": "Manual do Mundo", "link": "https://www.youtube.com/watch?v=vVjE_K5Xz8o", "dica": "Pequenos gastos, grandes rombos."},
        {"tema": "Cartão de Crédito sem sustos", "autor": "EconoMirna", "link": "https://www.youtube.com/watch?v=q6m09vjY0-o", "dica": "O cartão não é extensão do salário."},
        {"tema": "Imposto de Renda para Leigos", "autor": "Me Poupe!", "link": "https://www.youtube.com/watch?v=UqN93EwB0_Y", "dica": "Organize seus recibos anualmente."},
        {"tema": "Como comprar sua casa própria", "autor": "Primo Pobre", "link": "https://www.youtube.com/watch?v=mGzH_o6Y2qE", "dica": "Cuidado com o financiamento longo."},
        {"tema": "Tesouro Direto na Prática", "autor": "Jovens de Negócios", "link": "https://www.youtube.com/watch?v=S08xZ_2Fh_0", "dica": "Mais seguro que a poupança."}
    ]

    while True:
        exibir_cabecalho("Academia Easy Finance - Cursos Recomendados")
        for i, curso in enumerate(cursos, start=1):
            print(f"{i} - {curso['tema']} ({curso['autor']})")
        print(f"{RED}0 - Voltar{RESET}")
        print(f"{CYAN}{'='*63}{RESET}")

        escolha = input(f"\n{BOLD}Escolha um curso para detalhes ou 0 para voltar: {RESET}")

        if escolha == "0":
            break

        if escolha.isdigit() and 1 <= int(escolha) <= len(cursos):
            curso = cursos[int(escolha) - 1]
            print(f"\n{GREEN}{BOLD}📚 [CURSO: {curso['tema'].upper()}]{RESET}")
            print(f"👤 {BOLD}Autor:{RESET} {curso['autor']}")
            print(f"💡 Dica: {curso['dica']}")
            print(f"🔗 Assistir: {curso['link']}")
            input("\nPressione Enter para voltar ao menu...")
        else:
            print("⚠️ Opção inválida!")

