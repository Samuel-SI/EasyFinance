# src/services/i18n_service.py
import json
import os

class I18nService:
    def __init__(self, idioma="pt"):
        self.idioma_atual = idioma
        self.textos = {}
        
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_src = os.path.dirname(diretorio_atual)
        pasta_raiz = os.path.dirname(pasta_src)
        
        possiveis_caminhos = [
            os.path.join(pasta_src, "locales"),
            os.path.join(pasta_raiz, "locales"),
            os.path.join(pasta_src, "i18n"),
            os.path.join(pasta_raiz, "i18n")
        ]
        
        self.pasta_idiomas = None
        for caminho in possiveis_caminhos:
            if os.path.exists(caminho):
                self.pasta_idiomas = caminho
                print(f"🎯 SUCESSO: Pasta de traduções encontrada em: {self.pasta_idiomas}")
                break
                
        if not self.pasta_idiomas:
            print("❌ ERRO: Nenhuma pasta de JSON encontrada!")
            
        self.carregar_idioma(idioma)

    def carregar_idioma(self, sigla):
        if not self.pasta_idiomas:
            self.textos = {}
            return
        self.idioma_atual = sigla
        caminho_arquivo = os.path.join(self.pasta_idiomas, f"{sigla}.json")
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                self.textos = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            if sigla != "pt":
                self.carregar_idioma("pt")
            else:
                self.textos = {}

    def t(self, chave, **kwargs):
        """Busca a tradução e injeta parâmetros dinâmicos se fornecidos."""
        texto_base = self.textos.get(str(chave), str(chave))
        if kwargs:
            try:
                return texto_base.format(**kwargs)
            except KeyError as e:
                print(f"⚠️ Parâmetro {e} ausente na chave '{chave}'")
                return texto_base
        return texto_base
        
    def get(self, chave, padrao=None):
        return self.textos.get(str(chave), padrao if padrao is not None else str(chave))