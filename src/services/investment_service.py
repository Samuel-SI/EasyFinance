# src/services/investment_service.py
import urllib.request
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
class InvestmentService:
    def __init__(self, repository):
        self.repo = repository

    def obter_cotacao_moedas(self):
        """Busca a cotação atualizada do Dólar e Euro em tempo real via API nativa"""
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                dados = json.loads(response.read().decode())

                cotacoes = {
                    "USD": float(dados["USDBRL"]["bid"]),
                    "EUR": float(dados["EURBRL"]["bid"])
                }
                return cotacoes
        except Exception as e:
            print(f"Erro de conexão com a API de investimentos: {e}")
            return None

    def calcular_performance_ativo(self, ativo, cotacoes_api):
        """
        Executa a engenharia matemática do RF020.
        Calcula Lucro/Prejuízo bruto e percentual baseado na cotação em tempo real.
        """
        ticker = ativo.get('ticker', '').upper()
        qtd = float(ativo.get('quantidade', 0))
        preco_pago = float(ativo.get('preco_compra', 0))
        
        # Se for USD ou EUR, busca na API. Se for outro ativo ou API falhar, assume o preço pago (variação 0)
        cotacao_atual = preco_pago
        if cotacoes_api and ticker in cotacoes_api:
            cotacao_atual = cotacoes_api[ticker]
            
        custo_total = qtd * preco_pago
        valor_atual = qtd * cotacao_atual
        lucro_prejuizo = valor_atual - custo_total
        
        variacao_percentual = 0.0
        if custo_total > 0:
            variacao_percentual = (lucro_prejuizo / custo_total) * 100
            
        return {
            "custo_total": custo_total,
            "valor_atual": valor_atual,
            "lucro_prejuizo": lucro_prejuizo,
            "variacao_percentual": variacao_percentual,
            "cotacao_atual": cotacao_atual
        }

    def exportar_relatorio_txt(self, usuario, cotacoes_api):
        """
        Implementação do RF021 - Exportação de Relatório de Desempenho Patrimonial.
        Gera um arquivo .txt formatado na Área de Trabalho do usuário.
        """
        if not hasattr(usuario, 'investimentos') or not usuario.investimentos:
            return False, "O usuário não possui ativos para exportar."
            
        try:
            # Caminho padrão da área de trabalho do Windows/Linux/Mac de forma segura
            pasta_home = os.path.expanduser("~")
            caminho_desktop = os.path.join(pasta_home, "Desktop")
            
            # Se por acaso a pasta Desktop não existir, salva no diretório atual do projeto
            if not os.path.exists(caminho_desktop):
                caminho_desktop = os.getcwd()
                
            nome_arquivo = f"Relatorio_Investimentos_{usuario.email.split('@')[0]}.txt"
            caminho_final = os.path.join(caminho_desktop, nome_arquivo)
            
            patrimonio_total_pago = 0
            patrimonio_total_atual = 0
            
            with open(caminho_final, "w", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write("          EASYFINANCE - RELATÓRIO DE PERFORMANCE B2B\n")
                f.write(f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Conta Empresarial: {usuario.email}\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"COTAÇÕES DE REFERÊNCIA EM TEMPO REAL:\n")
                if cotacoes_api:
                    f.write(f" -> Dólar (USD): R$ {cotacoes_api.get('USD', 0):.2f}\n")
                    f.write(f" -> Euro (EUR): R$ {cotacoes_api.get('EUR', 0):.2f}\n")
                else:
                    f.write(" -> Cotações indisponíveis (Modo Offline)\n")
                f.write("-"*60 + "\n\n")
                
                f.write("DETALHAMENTO DA CARTEIRA CORPORATIVA:\n\n")
                
                for ativo in usuario.investimentos:
                    perf = self.calcular_performance_ativo(ativo, cotacoes_api)
                    
                    patrimonio_total_pago += perf["custo_total"]
                    patrimonio_total_atual += perf["valor_atual"]
                    
                    sinal = "+" if perf["lucro_prejuizo"] >= 0 else ""
                    
                    f.write(f"Ativo: {ativo['ticker']} | Qtd: {ativo['quantidade']} | Custo Unitário: R$ {ativo['preco_compra']:.2f}\n")
                    f.write(f" > Custo Inicial Investido: R$ {perf['custo_total']:.2f}\n")
                    f.write(f" > Valor de Mercado Atual: R$ {perf['valor_atual']:.2f} (Cotado a R$ {perf['cotacao_atual']:.2f})\n")
                    f.write(f" > Rendimento Consolidado: {sinal}R$ {perf['lucro_prejuizo']:.2f} ({sinal}{perf['variacao_percentual']:.2f}%)\n")
                    f.write("-" * 40 + "\n")
                
                lucro_total = patrimonio_total_atual - patrimonio_total_pago
                sinal_total = "+" if lucro_total >= 0 else ""
                var_total_perc = (lucro_total / patrimonio_total_pago * 100) if patrimonio_total_pago > 0 else 0
                
                f.write("\n" + "="*60 + "\n")
                f.write("RESUMO PATRIMONIAL DA EMPRESA:\n")
                f.write(f"Total Investido Inicial: R$ {patrimonio_total_pago:.2f}\n")
                f.write(f"Total Avaliado Atualmente: R$ {patrimonio_total_atual:.2f}\n")
                f.write(f"Resultado Líquido do Portfólio: {sinal_total}R$ {lucro_total:.2f} ({sinal_total}{var_total_perc:.2f}%)\n")
                f.write("="*60 + "\n")
                
            return True, caminho_final
        except Exception as e:
            return False, f"Erro ao gerar arquivo: {str(e)}"

    def enviar_relatorio_por_email(self, usuario, caminho_arquivo):
        """
        Dispara o arquivo PDF gerado diretamente para o e-mail cadastrado do usuário.
        """
        # Configurações do Servidor SMTP (Exemplo usando Gmail/Google Workspace)
        # ⚠️ IMPORTANTE: Lembre-se de gerar uma "Senha de App" de 16 dígitos nas configurações de segurança do Google.
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_REMETENTE = os.getenv("EMAIL_USER") 
        SENHA_REMETENTE = os.getenv("EMAIL_PASS") 

        destinatario = usuario.email

        try:
            # 1. Instancia e configura os metadados da mensagem corporativa
            msg = MIMEMultipart()
            msg['From'] = f"EasyFinance B2B <{EMAIL_REMETENTE}>"
            msg['To'] = destinatario
            msg['Subject'] = "📊 Seu Relatório Patrimonial Consolidado - EasyFinance"

            # 2. Constrói o corpo do e-mail com estrutura HTML premium
            corpo_html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <h2 style="color: #6366F1;">Olá, Gestor!</h2>
                    <p>Conforme solicitado na plataforma <b>EasyFinance</b>, compilamos o balanço patrimonial atualizado da sua empresa.</p>
                    <p>O arquivo consolidado contendo o desempenho da sua carteira de ativos e cálculos em tempo real encontra-se em anexo a esta mensagem.</p>
                    <br>
                    <p>Atenciosamente,<br><b>Equipe EasyFinance B2B</b></p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin-top: 30px;">
                    <p style="font-size: 11px; color: #777;">Este é um e-mail automático gerado pelo sistema. Por favor, não responda diretamente.</p>
                </body>
            </html>
            """
            msg.attach(MIMEText(corpo_html, 'html'))

            # 3. Valida a existência do PDF e o anexa em formato binário estável
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "rb") as f_anexo:
                    nome_exibicao = os.path.basename(caminho_arquivo)
                    
                    # MIMEApplication configura automaticamente as propriedades ideais para arquivos PDF
                    anexo = MIMEApplication(f_anexo.read(), Name=nome_exibicao)
                    anexo['Content-Disposition'] = f'attachment; filename="{nome_exibicao}"'
                    msg.attach(anexo)
            else:
                return False, "Arquivo de relatório não foi localizado para o anexo."

            # 4. Inicia sessão SMTP autenticada sob criptografia TLS
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            server.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
            server.quit()

            return True, "E-mail enviado com sucesso!"

        except Exception as e:
            return False, f"Falha ao processar o envio: {str(e)}"