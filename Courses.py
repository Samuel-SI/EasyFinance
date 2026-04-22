import webbrowser

class CourseManager:
    def __init__(self):
        self.cursos = [
            {"id": 1, "titulo": "Separação de Contas (PF vs PJ)", "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            {"id": 2, "titulo": "Fluxo de Caixa para Iniciantes", "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
            {"id": 3, "titulo": "Como precificar seu produto", "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        ]

    def exibir_aba(self):
        print("\n" + "="*40)
        print("   EDUCAÇÃO FINANCEIRA - EASYFINANCE   ")
        print("="*40)
        for c in self.cursos:
            print(f"[{c['id']}] {c['titulo']}")
        
        op = input("\nSelecione um curso para abrir ou '0' para voltar: ")
        if op.isdigit() and int(op) > 0:
            curso = next((c for c in self.cursos if c['id'] == int(op)), None)
            if curso:
                print(f"Abrindo curso: {curso['titulo']}...")
                webbrowser.open(curso['link'])