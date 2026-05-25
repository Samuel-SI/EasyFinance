import os
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from src.repository.json_repo import JsonRepository
from src.models.usuario import Usuario

load_dotenv()

class AuthService:
    """Verifica se um email já está cadastrado (Útil para o cadastro)."""

    def __init__(self, repository: JsonRepository):
        self.repo = repository

    def cadastrar_usuario(self, email: str, documento: str, senha: str) -> tuple:
        """Valida e registra um novo microempreendedor no sistema."""
        if self.repo.email_existe(email):
            return False, "Este e-mail já está cadastrado no EasyFinance."
        
        novo_usuario = Usuario(email=email, documento=documento, senha=senha)

        self.repo.salvar_usuario(novo_usuario)
        return True, "Cadastro realizado com sucesso!"

    def realizar_login(self, email: str, senha: str) -> tuple:
        """Verifica as credenciais e retorna o Objeto Usuario caso estejam corretas."""
        usuario = self.repo.buscar_usuario_por_email(email)

        if not usuario:
            return False, "Usuário não encontrado em nossa base de dados."
        
        if usuario.senha != senha:
            return False, "Senha incorreta. Tente novamente."
        
        return True, usuario
    
    def enviar_2fa_email(self, email_destino):
        """Gera um código e envia via SMTP do Gmail"""
        codigo = str(random.randint(100000, 999999))

        email_origem = os.getenv("EMAIL_USER")
        senha_app = os.getenv("EMAIL_PASS")

        msg = EmailMessage()
        msg['subject'] = "🔐 Código de Segurança - Easy Finance"
        msg['from'] = email_origem
        msg['to'] = email_destino

        conteudo = f"""Olá!
        
        O seu código de segurança para acessar o Easy Finance é: {codigo}
        
        Se não solicitou este código, por favor ignore este e-mail.
        """
        msg.set_content(conteudo)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_origem, senha_app)
                smtp.send_message(msg)

            print(f" (log do sistema: E-mail de segurança enviado para {email_destino}")
            return codigo
        except Exception as e:
            print(f"Erro técnico ao enviar e-mail {e}")
            return None 