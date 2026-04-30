# 💹 Easy Finance — Controle seu Futuro

O **Easy Finance** é uma aplicação em Python desenvolvida para oferecer uma gestão financeira prática, segura e modular. Diferente de planilhas convencionais, o sistema foca na automação de alertas e na proteção de dados do usuário através de camadas de segurança e validações rigorosas.

---

## 🛠️ Funcionalidades Elaboradas

O projeto foi construído com foco em **Lógica Modular** e **Clean Code**, apresentando as seguintes funcionalidades:

* **🛡️ Camada de Segurança (2FA):** Sistema de verificação em duas etapas que gera tokens dinâmicos para validar o acesso do usuário, garantindo que apenas o proprietário da conta visualize os dados.
* **📅 Painel de Prazos Inteligente:** Monitoramento automático que lê a data atual do sistema e sinaliza contas críticas ou próximas do vencimento.
* **💰 Gestão de Fluxo de Caixa:** Registro detalhado de entradas e saídas com cálculo imediato de saldo líquido.
* **📂 Persistência de Dados Inteligente:** Organização de arquivos individuais em formato `.txt` dentro da pasta `data/`, permitindo que os dados não se percam após fechar o programa.
* **✅ Validador de Acesso:** Implementação de máscaras de entrada via Expressões Regulares (Regex) para garantir que e-mails e CPFs estejam sempre no formato correto.
* **🎯 Planejador de Metas:** Módulo para registro e acompanhamento de objetivos financeiros de curto e longo prazo.

---

## 📦 Tecnologias e Bibliotecas

Para garantir leveza e eficiência, o projeto utiliza exclusivamente as bibliotecas nativas do **Python 3**:

| Biblioteca | Objetivo |
| :--- | :--- |
| `datetime` | Crucial para a lógica de vencimentos e cálculos de dias restantes. |
| `random` | Responsável pela geração dos códigos dinâmicos do 2FA. |
| `os` & `sys` | Gerenciamento de pastas, limpeza de tela e importação de módulos. |
| `ast` | Utilizada no carregamento de dados para interpretar dicionários salvos em texto. |
| `re` | Implementação de máscaras de validação para dados de cadastro. |

---

## 📂 Organização do Projeto (Estrutura)

A separação de responsabilidades foi aplicada para facilitar a manutenção:

* `main.py`: Ponto de partida e controle de fluxo inicial.
* `src/finance_engine.py`: Onde os cálculos e alertas de prazos acontecem.
* `src/database.py`: Lógica de salvamento e carregamento de arquivos TXT.
* `src/security.py`: Módulo exclusivo para a proteção da conta (2FA).
* `src/interface.py`: Gerenciamento de menus e interação com o usuário.
* `src/validators.py`: Regras de negócio para validação de login e cadastros.

---

## 🚀 Detalhes de Instalação e Execução

Como o projeto utiliza apenas bibliotecas padrão, a instalação é simples:

1.  **Clone este repositório:**
    ```bash
    git clone [https://github.com/Samuel-SI/EasyFinance.git](https://github.com/Samuel-SI/EasyFinance.git)
    ```
2.  **Navegue até a pasta do projeto:**
    ```bash
    cd easy-finance
    ```
3.  **Execute o sistema:**
    ```bash
    python main.py
    ```

---

## 👥 Time de Desenvolvimento
* **Samuel Rocha**
* **Richard Carmo**

## 🔗 Links Extras
* [Documentação Complementar (Google Drive)](https://drive.google.com/drive/folders/1wf95DX--Q_ywYsi8r6SW_D9cAkNzfT3J?usp=drive_link)



*Dabliu essi é um cara legal*