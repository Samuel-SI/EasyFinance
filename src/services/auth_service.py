# src/services/auth_service.py
"""
Módulo de serviços responsável por concentrar a lógica de negócio de Autenticação.
Lida com cadastro de usuários, validação de login e envio de códigos de verificação em duas etapas (2FA).
"""

import os
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from src.repository.json_repo import JsonRepository
from src.models.usuario import Usuario

# Carrega as variáveis de ambiente do arquivo .env (ex: senhas e e-mails do sistema)
load_dotenv()

class AuthService:
    """
    Serviço que orquestra o fluxo de autenticação e segurança.
    Atua como uma ponte entre as telas (Views) e o banco de dados (Repository).
    """

    def __init__(self, repository: JsonRepository):
        """
        Inicializa o serviço injetando a dependência do repositório de dados.
        
        Args:
            repository (JsonRepository): Instância do repositório responsável pelas operações de I/O.
        """
        self.repo = repository

    def cadastrar_usuario(self, email: str, documento: str, senha: str) -> tuple:
        """
        Valida e registra um novo microempreendedor no sistema.
        
        Args:
            email (str): E-mail fornecido pelo usuário.
            documento (str): CPF ou CNPJ do usuário.
            senha (str): Senha escolhida.
            
        Returns:
            tuple: (Booleano indicando sucesso, Mensagem de feedback)
        """
        # Regra de Negócio: O e-mail é a chave única. Não pode haver duplicidade.
        if self.repo.email_existe(email):
            return False, "Este e-mail já está cadastrado no EasyFinance."
        
        # Instancia um novo objeto Usuario com os dados fornecidos
        novo_usuario = Usuario(email=email, documento=documento, senha=senha)

        # Solicita ao repositório que grave o novo usuário no banco de dados (JSON)
        self.repo.salvar_usuario(novo_usuario)
        return True, "Cadastro realizado com sucesso!"

    def realizar_login(self, email: str, senha: str) -> tuple:
        """
        Verifica as credenciais e retorna o Objeto Usuario caso estejam corretas.
        
        Args:
            email (str): E-mail digitado no login.
            senha (str): Senha digitada no login.
            
        Returns:
            tuple: (Sucesso booleano, Objeto Usuario em caso de sucesso OU mensagem de erro)
        """
        # Busca o cadastro do usuário no banco de dados pelo e-mail
        usuario = self.repo.buscar_usuario_por_email(email)

        # Se o repositório retornar None, o usuário não existe
        if not usuario:
            return False, "Usuário não encontrado em nossa base de dados."
        
        # Valida se a senha digitada bate com a senha armazenada no objeto
        if usuario.senha != senha:
            return False, "Senha incorreta. Tente novamente."
        
        # Login bem-sucedido: retorna True e a própria instância do usuário para a sessão
        return True, usuario
    
    def enviar_2fa_email(self, email_destino):
        """
        Gera um código de segurança aleatório de 6 dígitos e envia via SMTP do Gmail.
        Usado para a Verificação em Duas Etapas (2FA).
        
        Args:
            email_destino (str): Endereço de e-mail do usuário que solicitou o login.
            
        Returns:
            str ou None: O código gerado caso o envio tenha sucesso, ou None se falhar.
        """
        # Gera uma string numérica aleatória de 6 dígitos (ex: "482019")
        codigo = str(random.randint(100000, 999999))

        # Recupera as credenciais do sistema armazenadas com segurança no .env
        email_origem = os.getenv("EMAIL_USER")
        senha_app = os.getenv("EMAIL_PASS") # Deve ser uma "Senha de App" gerada no Google, não a senha comum

        # Constrói o corpo do e-mail
        msg = EmailMessage()
        msg['subject'] = "🔐 Código de Segurança - Easy Finance"
        msg['from'] = email_origem
        msg['to'] = email_destino

        # Define a mensagem (Interpola o código gerado no texto)
        conteudo = f"""Olá!
        
        O seu código de segurança para acessar o Easy Finance é: {codigo}
        
        Se não solicitou este código, por favor ignore este e-mail.
        """
        msg.set_content(conteudo)

        try:
            # Estabelece uma conexão segura (SSL) com o servidor SMTP do Gmail na porta 465
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_origem, senha_app) # Autentica a conta do sistema
                smtp.send_message(msg)              # Dispara o e-mail

            # Log para debug/monitoramento interno (aparece apenas no terminal)
            print(f" (log do sistema: E-mail de segurança enviado para {email_destino})")
            
            # Retorna o código gerado para que a interface exija a validação do mesmo
            return codigo
            
        except Exception as e:
            # Captura qualquer erro de rede, autenticação ou bloqueio do provedor
            print(f"Erro técnico ao enviar e-mail: {e}")
            return None