import json
import os
from src.models.usuario import Usuario

DB_PATH = os.path.join('data', 'database.json')

class JsonRepository:
    """Gerencia a persistência dos Objetos no arquivo JSON."""
    def __init__(self):
        self._inicializar_banco()

    def _inicializar_banco(self):
        if not os.path.exists('data'):
            os.makedirs('data', exist_ok=True)
        if not os.path.exists(DB_PATH):
            estrutura = {"usuarios_cadastrados": {}, "repositorio_dados": {}}
            with open(DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(estrutura, f, indente= 4, ensure_ascii=False)
    
    def _ler_banco(self) -> dict:
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()
                if not conteudo:
                    return {"usuarios_cadastrados": {}, "repositorio_dados": {}}
                return json.loads(conteudo)
        except Exception as e:
            print(f"Erro ao ler o banco de dados: {e}")
            return {"usuarios_cadastrados": {}, "repositorio_dados": {}}
        
    def _salvar_banco(self, dados: dict):
        try:
            with open(DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar o banco de dados: {e}")

    def buscar_usuario_por_email(self, email: str) -> Usuario:
        """Busca no JSON e retorna uma instância completa do Objeto Usuario."""
        db = self._ler_banco()
        usuarios = db.get("usuarios_cadastrados", {})

        if email not in usuarios:
            return None
        doc = usuarios[email].get("documento", "")
        senha = usuarios[email].get("senha", "")

        usuario = Usuario(email, doc, senha)

        dados_repo = db.get("repositorio_dados", {}).get(email, {})
        usuario.carregar_dados_do_dicionario(dados_repo)

        return usuario
    
    def salvar_usuario(self, usuario):
        """Pega o Objeto Usuario modificado e injeta de volta no JSON."""
        db = self._ler_banco()
        
        # Garante que as chaves principais existam no dicionário antes de salvar
        if "usuarios_cadastrados" not in db:
            db["usuarios_cadastrados"] = {}
        if "repositorio_dados" not in db:
            db["repositorio_dados"] = {}
            
        # Salva as informações de autenticação (Login)
        db["usuarios_cadastrados"][usuario.email] = {
            "senha": usuario.senha,
            "documento": usuario.documento
        }
        
        # Salva os dados de progresso e gamificação (Metas, Pontos, etc.)
        db["repositorio_dados"][usuario.email] = usuario.serializar_dados()
        
        # Grava fisicamente no arquivo JSON
        self._salvar_banco(db)

    def obter_ranking_empresarial(self) -> list:
        """Gera o ranking anônimo de usuários para a Gamificação (B2B)."""
        db = self._ler_banco()
        ranking = []

        for email, dados in db.get("repositorio_dados", {}) .items():
            partes = email.split("@")
            mascara = partes[0][:2] + "***@" + partes [1] if len(partes[0]) > 2 else "***@" + partes[1]

            pontos = dados.get("pontos", 0)
            nivel = dados.get("nivel", "Bronze")
            ranking.append({"empresa": mascara, "pontos": pontos, "nivel": nivel})

        return sorted(ranking, key=lambda x: x["pontos"], reverse=True)
    def email_existe(self, email: str) -> bool:
        """Verifica se um email já está cadastrado (Útil para o cadastro)."""
        db = self._ler_banco()
        return email in db.get("usuarios_cadastrados", {})