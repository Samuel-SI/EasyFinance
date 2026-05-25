import os
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from src.utils.visual import BOLD, RED, RESET, GREEN

load_dotenv()

def enviar_2fa_email(email_destino):
    """Gera um código e envia via SMTP do Gmail"""
    codigo = str(random.randint(100000, 999999))

    email_origem = os.getenv("EMAIL_USER")
    senha_app = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg['subject'] = "🔐 Código de Segurança - Easy Finance"
    msg['from'] = email_origem
    msg['to'] = email_destino
    
    conteudo = f"""
    Olá!
    
    O seu código de segurança para aceder ao Easy Finance é: {codigo}
    
    Se não solicitou este código, por favor ignore este e-mail.
    """
    msg.set_content(conteudo)

    # REPARE: O try agora está indentado para dentro da função!
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_origem, senha_app)
            smtp.send_message(msg)
        
        print(f"✅ E-mail enviado com sucesso para {email_destino}!")
        return codigo  # Retorna o código para a verificação usar
    except Exception as e:
        print(f"\n{RED}Erro técnico ao enviar e-mail: {e}{RESET}")
        return None

    


def verificar_2fa(email_usuario):
    """
    Gera um código aleatório e solicita a confirmação do usuário.
    Em um sistema real, este código seria enviado por e-mail ou SMS.
    """
    # Gera um código de 6 dígitos
    codigo_gerado = enviar_2fa_email(email_usuario)
    if not codigo_gerado:
        print(f"{RED}Não foi possível enviar o código de segurança. Tente novamente mais tarde. {RESET}")
        return False
    
    print(f"\n{BOLD}--- AUTENTICAÇÃO DE DOIS FATORES ---{RESET}")

    tentativas = 3
    while tentativas >0:
        codigo_inserido = input("\nDigite o código de segurança enviado para seu e-mail: ").strip()

        if codigo_inserido == codigo_gerado:
            print(f"{GREEN}✅ Código correto! Acesso concedido.{RESET}")
            return True
        else:
            tentativas -= 1
            print(f"{RED}❌ Código incorreto! Você tem mais {tentativas} tentativas.{RESET}")
    print(f"{RED}🚨 Acesso bloqueado: Muitas tentativas falhas.{RESET}")
    return False
