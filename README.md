💹 Easy Finance - Controle seu Futuro

Propósito do Projeto: > Criar uma ferramenta prática e segura para quem precisa organizar a vida financeira sem complicação. O foco foi aplicar lógica modular em Python para gerenciar gastos, prazos e metas, garantindo que os dados não se percam e fiquem protegidos.

🛠️ Funcionalidades do Sistema:

🛡️ Camada de Segurança (2FA): Sistema de verificação em duas etapas que gera tokens aleatórios para validar o acesso.

📅 Painel de Prazos: Monitoramento automático de datas. O sistema lê o calendário do computador e sinaliza contas críticas.

💰 Gestão de Fluxo: Cadastro de entradas e saídas com cálculo de saldo líquido imediato.

📂 Banco de Dados em TXT: Persistência de dados inteligente que organiza arquivos individuais para cada usuário na pasta data/.

✅ Validador de Acesso: Filtros de segurança para garantir que e-mails e CPFs sejam digitados no formato correto.

🎯 Planejador de Metas: Módulo para registro de objetivos financeiros de curto e longo prazo.

📦 Tecnologias e Bibliotecas
Para este projeto, focamos em utilizar as bibliotecas nativas do Python 3, garantindo leveza e eficiência:

datetime → Crucial para a lógica de vencimentos e cálculos de dias restantes.

random → Responsável pela geração dos códigos dinâmicos do 2FA.

os & sys → Gerenciamento de pastas, limpeza de tela e importação dos módulos da pasta src.

ast → Utilizada no carregamento de dados para interpretar listas e dicionários salvos nos arquivos.

re (Regular Expressions) → Para criar as "máscaras" de validação de dados de cadastro.

📂 Como o código está dividido?
O projeto foi construído seguindo o conceito de Clean Code, separando a interface da lógica:

main.py ➔ Ponto de partida e controle de fluxo inicial.

src/finance_engine.py ➔ Onde os cálculos e alertas acontecem.

src/database.py ➔ Toda a lógica de salvar e carregar arquivos.

src/security.py ➔ Módulo exclusivo para a proteção da conta (2FA).

src/interface.py ➔ Gerencia os menus e a interação com o usuário.

src/validators.py ➔ Regras de negócio para login e novos cadastros.

🚀 Execução
Para rodar o gestor, utilize o comando:
python main.py

📈 Evolução (Backlog)
[ ] Integração com SQLite para substituir os arquivos de texto.

[ ] Envio automático de comprovantes por e-mail.

[ ] Dashboard visual com gráficos de pizza para gastos mensais.

[ ] Interface gráfica para uma melhor experiência

👥 Time de Desenvolvimento
Samuel Rocha

Richard Carmo
