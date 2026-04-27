import random

def verificar_2fa(email_usuario):
    """
    Gera um código aleatório e solicita a confirmação do usuário.
    Em um sistema real, este código seria enviado por e-mail ou SMS.
    """
    # Gera um código de 6 dígitos
    codigo_gerado = str(random.randint(100000, 999999))
    
    print(f"\n--- AUTENTICAÇÃO DE DOIS FATORES ---")
    print(f"Um código de segurança foi enviado para: {email_usuario}")
    
    # SIMULAÇÃO: Para fins de teste no terminal, vamos exibir o código
    # Em produção, você removeria o print abaixo.
    print(f"[SIMULAÇÃO DE E-MAIL] Seu código é: {codigo_gerado}")
    
    tentativas = 3
    while tentativas > 0:
        codigo_inserido = input("\nDigite o código de 6 dígitos: ")
        
        if codigo_inserido == codigo_gerado:
            print("✅ Identidade confirmada!")
            return True
        else:
            tentativas -= 1
            print(f"❌ Código incorreto! Você tem mais {tentativas} tentativas.")
            
    print("🚨 Acesso bloqueado: Muitas tentativas falhas.")
    return False