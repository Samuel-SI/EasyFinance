# 💹 Easy Finance — Controle seu Futuro

O **Easy Finance** é uma aplicação de gestão financeira empresarial projetada em Python, focada em fornecer controle prático, seguro e modular para micro e pequenas empresas (MPEs). 

O projeto foi construído de forma evolutiva ao longo de três etapas letivas (VAs), partindo de um protótipo inicial baseado em linha de comando (Terminal) até se tornar um ecossistema desktop moderno estruturado sob o paradigma de Programação Orientada a Objetos (POO), com persistência em banco de dados relacional, internacionalização e inteligência de negócios.

---

## 👥 Autores e Desenvolvedores
* **Samuel Rocha** — [GitHub](https://github.com/Samuel-SI)
* **Richard Carmo** — [GitHub](https://github.com/Richard-Carmo)

---

## 📸 Demonstração Visual da Interface (GUI atual)

O sistema atual conta com uma interface gráfica responsiva que se adapta nativamente ao Modo Escuro (*Dark Mode*) do sistema operacional.

| Tela de Diagnóstico & Teto de Gastos | Academia de Cursos Gamificada |
| :---: | :---: |
| ![Aba Diagnóstico](https://via.placeholder.com/400x250.png?text=Inserir+Print+do+Diagnostico) | ![Aba Cursos](https://via.placeholder.com/400x250.png?text=Inserir+Print+dos+Cursos) |

| Painel de Configurações & i18n | Carteira de Investimentos ao Vivo |
| :---: | :---: |
| ![Aba Configurações](https://via.placeholder.com/400x250.png?text=Inserir+Print+das+Configuracoes) | ![Aba Investimentos](https://via.placeholder.com/400x250.png?text=Inserir+Print+dos+Investimentos) |

---

## ⏳ 1ª Release (1ª VA) — O Protótipo Base (Modo Terminal)

Nesta primeira fase do projeto, o foco esteve na validação das regras de negócio básicas e na implementação de uma estrutura funcional operando via console de comandos (Terminal), utilizando arquivos de texto plano (`.txt`) para persistência de dados.

### 🛠️ Funcionalidades da 1ª Release:
* **RF001 — Menu Inicial (Autenticação):** O usuário insere e-mail e senha; o sistema realiza validações estritas de credenciais para conceder o acesso. Caso o banco de dados esteja vazio ou os dados incorretos, barra o acesso informando o motivo.
* **RF002 — Cadastro de Usuário (CRUD):** Permite a criação de uma conta corporativa com validações de formato rígidas:
  * *E-mail:* Validação de formato (presença de `@`, `.com`, sem espaços) e garantia de unicidade no sistema.
  * *Senha:* Exigência de 7 a 16 caracteres, contendo pelo menos um número e uma letra maiúscula, além de checagem de confirmação de senha idêntica.
  * *CPF/CNPJ:* Validação estrutural e barramento de documentos duplicados.
* **RF003 — Menu Principal:** Painel que gerencia a navegação entre as 6 ferramentas financeiras iniciais do usuário, salvando os dados automaticamente ao retornar para o menu.
* **RF004 — Registro de Entrada e Saída:** Registro manual de movimentações financeiras de fluxo de caixa (entradas e saídas) atualizando o saldo disponível imediatamente.
* **RF005 — Gestão de Contas a Pagar/Receber:** Cadastro de lembretes financeiros que alertam o utilizador sobre contas com vencimento no dia atual ou nos próximos dias utilizando um sistema de alertas.
* **RF006 — Geração de Relatórios:** Comparativo matemático básico de receitas e despesas semanais para avaliar o crescimento do negócio.
* **RF007 — Alertas Semanais de Situação (Diagnóstico):** Motor lógico que analisa o desempenho financeiro das últimas semanas e dá um veredito sobre a estabilidade ou necessidade de contenção de custos.
* **RF008 — Dashboard de Relatórios:** Resumo matemático consolidando todas as movimentações e apresentando o saldo líquido final, exibindo um ícone de alerta caso o caixa esteja negativo.
* **RF009 — Encerrar Sessão:** Mecanismo seguro de logout que limpa a memória temporária da sessão e retorna o utilizador ao fluxo de login inicial, prevenindo acessos não autorizados.
* **RF010 — Aba de Cursos:** Apresentação de uma lista de temas educativos focados em microempreendedorismo com links para vídeos de especialistas externos.
* **RF011 — Aba de Metas:** Módulo focado no cadastro e acompanhamento de objetivos e valores financeiros de forma organizada em listas numeradas.
* **Autenticação de Dois Fatores (2FA Lógico):** Geração de um token secreto temporário de 6 dígitos que deve ser inserido corretamente para liberar o acesso ao sistema. O código é simulado no próprio console para fins de teste.

---

## 🚀 2ª Release (2ª VA) — A Transição Desktop e Arquitetura POO

A segunda fase marcou a reengenharia completa do ecossistema. O terminal foi inteiramente substituído por uma interface gráfica de usuário (GUI) moderna e o código foi reestruturado sob a Programação Orientada a Objetos (POO), utilizando o banco de dados relacional SQLite.

### 🛠️ Funcionalidades da 2ª Release:
* **RF027 — Passagem para POO (Programação Orientada ao Objeto):** Reestruturação completa do código-fonte para o paradigma orientado a objetos, garantindo modularidade, reutilização de código e melhor manutenção.
* **ENH001 — Mascaramento Dinâmico de Senha (Toggle View):** Inclusão de um componente visual (CheckBox) que alterna a visibilidade dos caracteres da senha nas telas de login e cadastro.
* **RF013 — Sistema de Recompensa por Aprendizado (XP):** Mecanismo de gamificação que concede 20 pontos de experiência (XP) ao utilizador ao clicar em "Assistir" a um curso, bloqueando a duplicação de pontos em aulas concluídas.
* **RF014 — Atualização Dinâmica de Nível (Ranking B2B):** Motor de pontuação que acumula o XP ganho nos cursos e atualiza a classificação de perfil da empresa entre os níveis *Bronze, Prata, Ouro, Platina, Diamante e Diamante Vermelho*.
* **RF015 — Módulo de Edição de Perfil Corporativo:** Permite a alteração segura do documento (CPF/CNPJ) e a redefinição de senhas com travas contra campos em branco.
* **RF016 — Aba de Investimentos:** Interface exclusiva que possibilita ao gestor cadastrar, visualizar e gerenciar a carteira de investimentos da empresa.
* **RF017 — Consulta de Cotações em Tempo Real (Via API):** Integração via requisições de rede para capturar e exibir de forma automática cotações ao vivo de moedas e ativos, utilizando cache local em caso de ausência de internet.
* **RF018 — Simulador de Rendimento de Caixa (Renda Fixa):** Mecanismo de projeção de lucros futuros baseado em taxas de juros de referência (CDI/Selic), exibindo um comparativo gráfico direto com o rendimento da poupança.
* **RF019 — Registro de Compras de Ativos (Carteira):** Persistência estruturada no SQLite contendo quantidade, código do ativo e preço médio pago pela empresa, travando valores inválidos ou negativos.
* **RF020 — Painel de Lucro/Prejuízo Patrimonial:** Módulo inteligente que realiza o cruzamento do preço médio de custo da carteira com a API de mercado em tempo real, indicando a valorização total através de indicadores coloridos.
* **RF021 — Alerta de Custo de Oportunidade no Dashboard:** Monitoramento automático que exibe um alerta gráfico na tela principal do sistema caso a empresa mantenha uma quantia excessiva de capital parada em conta corrente sem render.

---

## 📊 3ª Release (3ª VA) — Inteligência de Mercado e Engenharia de Dados

Na terceira etapa letiva, o projeto incorporou recursos analíticos avançados, automação cambial e interfaces responsivas para garantir previsibilidade e gestão de riscos orçamentários.

### 🛠️ Funcionalidades da 3ª Release:
* **RF022 — Exportação de Relatórios e Carteira:** Mecanismo integrado para a geração e download de arquivos físicos (PDF/CSV/Excel) formatados com o histórico analítico de transações e investimentos do usuário.
* **RF023 — Conversor de Moedas Comercial Automatizado:** Conversão instantânea de valores corporativos de Reais para moedas estrangeiras (Dólar/Euro) com dados consumidos em tempo real via API.
* **RF024 — Rebalanceamento de Carteira (Metas):** Algoritmo inteligente que analisa e compara a distribuição patrimonial atual da empresa com as metas ideais estipuladas pelo gestor, sugerindo onde alocar novos aportes.
* **RF025 — Gráfico de Evolução Patrimonial Integrado:** Plotagem visual responsiva (Matplotlib) que gera um gráfico de linha consolidando a evolução temporal do somatório de caixa e carteira mês a mês.
* **RF026 — Controle de Teto de Gastos (Budgeting):** Gerenciamento e limitação de orçamento por categorias de despesa. O sistema exibe barras de progresso percentuais e altera dinamicamente as cores de componentes na tela (`Amarelo / Vermelho Alerta`) caso o teto orçamentário definido seja estourado.

---

## 📦 Matriz de Dependências Tecnológicas

| Tecnologia | Tipo | Finalidade no Projeto | Releases |
| :--- | :--- | :--- | :---: |
| **Python 3.10+** | Linguagem | Núcleo de desenvolvimento de toda a aplicação. | 1, 2 e 3 |
| **CustomTkinter** | Biblioteca Externa | Construção da interface desktop moderna e customizável. | 2 e 3 |
| **SQLite3** | Biblioteca Nativa | Armazenamento relacional e persistência de dados com transações seguras. | 2 e 3 |
| **smtplib / ssl** | Biblioteca Nativa | Conexão autenticada via servidor de e-mail corporativo para envio real do token 2FA. | 2 e 3 |
| **urllib.request / json**| Biblioteca Nativa | Consumo e tratamento de dados obtidos nas APIs REST de cotações financeiras. | 2 e 3 |
| **re** | Biblioteca Nativa | Processamento de Expressões Regulares para máscaras rígidas de entrada e validação. | 1, 2 e 3 |
| **hashlib** | Biblioteca Nativa | Criptografia (hashing) de senhas para gravação protegida no banco. | 2 e 3 |

---

## 📂 Arquitetura do Projeto (Árvore de Diretórios)

A organização adota os preceitos de Engenharia de Software baseados em separação estrita de conceitos e responsabilidades em camadas:

```text
├── main.py                    # Script principal e inicialização do sistema
├── easyfinance.db             # Banco de dados local SQLite3 (Gerado via código / Protegido no Git)
├── locales/                   # Arquivos estruturados JSON para i18n (pt, en, es, fr)
└── src/
    ├── models/                # Entidades estruturadas (Usuario, Transacao, Meta, Lembrete)
    ├── repository/            # Camada de persistência isolada e consultas SQL (sqlite_repo.py)
    ├── services/              # Lógica de negócio (Auth, Finance, i18n, Investment)
    ├── views/                 # Componentes visuais, Frames e CustomWidgets do CustomTkinter
    ├── utils/                 # Scripts auxiliares e formatadores de strings
    └── legado/                # Módulos históricos originais construídos via Terminal na Unidade 1
```

## 🚀 Guia de Instalação e Execução
📋 Pré-requisitos
Ter o Python instalado em seu computador (Versão 3.10 ou superior recomendada).
Conexão ativa com a internet (necessária para as cotações de moedas ao vivo e o envio de e-mails do 2FA).

## 🛠️ Passo a Passo para Execução
Siga os comandos abaixo no seu terminal para baixar, configurar e rodar o projeto localmente:

Clone este repositório do GitHub:
 ```bash
    git clone [https://github.com/Samuel-SI/EasyFinance.git](https://github.com/Samuel-SI/EasyFinance.git)

Acesse a pasta do projeto que foi baixada:
```bash
    cd EasyFinance

Crie e ative um Ambiente Virtual (Venv) para isolar as dependências:

No Windows:
```bash
    python -m venv venv
    .\venv\Scripts\activate

No Linux ou macOS:
```bash
    python3 -m venv venv
    source venv/bin/activate

Instale a biblioteca gráfica necessária para a interface rodar:
```bash
    pip install customtkinter

Inicie a aplicação:
```bash
    python main.py
```
## ⚙️ Workflow do Git (Versionamento):
Para assegurar o desenvolvimento síncrono limpo e evitar conflitos destrutivos durante a integração do código, a dupla adotou o fluxo de trabalho baseado em Feature Branches:

Branch main: Retém exclusivamente o código estável, homologado e pronto para apresentação.

Branches de Funcionalidades (feat/): Cada nova tela ou serviço foi desenvolvido em uma ramificação isolada.

Fluxo de Trabalho Prático no Terminal:

Antes de iniciar uma nova tarefa, atualize sua branch principal:
```bash
    git checkout main
    git pull origin main

Crie uma nova branch para a funcionalidade que vai desenvolver:
```bash
    git checkout -b feat/nome-da-sua-funcionalidade

Após finalizar as alterações no código, adicione e envie para o GitHub:
```bash
    git add .
    git commit -m "feat: adiciona descricao clara da funcionalidade"
    git push origin feat/nome-da-sua-funcionalidade
    Integração: Abra um Pull Request no GitHub para que a dupla revise o código antes de juntar as alterações na branch main.
```
## 🔗 Links e Recursos Extras##
📂 Documentação Complementar: Acesse todos os relatórios estruturados, diagramas e notas de planejamento na Pasta do Projeto no Google Drive. 

📦 Artigo do Overleaf: Entenda o processo todo em um artigo científico pelo link: https://www.overleaf.com/project/6a047b8469358960a21c5d65