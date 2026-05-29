# src/utils/tradutor.py

# Importamos os dicionários dos arquivos separados
from src.utils.lang_pt import TEXTOS_PT
from src.utils.lang_en import TEXTOS_EN
from src.utils.lang_es import TEXTOS_ES
from src.utils.lang_fr import TEXTOS_FR

class Tradutor:
    IDIOMA_ATUAL = "pt"

    # O sistema junta os arquivos aqui automaticamente
    TEXTOS = {
        "pt": TEXTOS_PT,
        "en": TEXTOS_EN,
        "es": TEXTOS_ES,
        "fr": TEXTOS_FR
    }

    @classmethod
    def t(cls, chave, fallback=None):
        """Retorna o termo traduzido. Se não existir, retorna o fallback (ou a própria chave)."""
        dic_idioma = cls.TEXTOS.get(cls.IDIOMA_ATUAL, cls.TEXTOS["pt"])
        if fallback:
            return dic_idioma.get(chave, fallback)
        return dic_idioma.get(chave, chave)

    @classmethod
    def mudar_idioma(cls, novo_idioma):
        """Muda o idioma global instantaneamente"""
        if novo_idioma in cls.TEXTOS:
            cls.IDIOMA_ATUAL = novo_idioma