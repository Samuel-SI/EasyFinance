# 💰 Easy Finance - Gestor Financeiro Pessoal

Sistema de gestão financeira desenvolvido em Python como projeto principal para a Verificação de Aprendizagem . O software foca no controle de fluxo de caixa, planejamento de metas e gestão inteligente de prazos.

## 🚀 Funcionalidades

* **Fluxo de Caixa:** Registro detalhado de entradas e saídas com atualização de saldo em tempo real.
* **Alertas de Vencimento Dinâmicos:** O sistema utiliza a data atual do computador para calcular quantos dias faltam para um pagamento, categorizando o risco por cores (🟢, 🟡, 🔴).
* **Gestão de Metas:** Cadastro de objetivos financeiros utilizando estruturas de dicionários.
* **Persistência Robusta:** Sistema de salvamento automático em arquivos `.txt` que suporta acentuação brasileira e evita corrupção de dados.

## 🛠️ Tecnologias e Conceitos Aplicados

* **Linguagem:** Python 3.14+
* **Manipulação de Datas:** Biblioteca `datetime` para aritmética de prazos.
* **Estruturas de Dados:** Uso intensivo de **Dicionários** e **Listas** para organização de objetos complexos.
* **Tratamento de Exceções:** Implementação de blocos `try-except` e validações `isinstance` para evitar crashes por dados mal formatados.
* **Encoding:** Padronização em `latin-1` com tratamento de erros de codec para compatibilidade entre sistemas operacionais.

## 📁 Estrutura de Pastas

```text
Projeto EasyFinance/
├── main.py              # Menu principal e orquestração do sistema
├── data/                # Banco de dados (.txt)
└── src/                 # Módulos de lógica do sistema
    ├── database.py      # Funções de carga e salvamento (Persistência)
    ├── finance_engine.py # Motor de cálculos e alertas
    ├── goals.py          # Gerenciamento de metas
    ├── Courses.py        # Módulo de conteúdo educativo
    └── validators.py     # Lógica de login e cadastro