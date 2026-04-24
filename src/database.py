import json
import os


CAMINHO_USUARIOS = "data/usuarios.csv"
CAMINHO_TRANSACOES = "data/transacoes.csv"
# src/database.py
import os

def salvar_dados(nome_arquivo, lista_dados):
    # Garante que a pasta 'data' existe
    if not os.path.exists('data'):
        os.makedirs('data')
        
    caminho = os.path.join('data', nome_arquivo)
    with open(caminho, 'w') as f:
        for item in lista_dados:
            f.write(f"{item}\n")

def carregar_dados(nome_arquivo):
    caminho = os.path.join('data', nome_arquivo)
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, 'r') as f:
        # Lê cada linha e remove o '\n'
        return [linha.strip() for linha in f.readlines()]

def salvar_valores_financeiros(nome_arquivo, lista_valores):
    if not os.path.exists('data'):
        os.makedirs('data')
        
    caminho = os.path.join('data', nome_arquivo)
    with open(caminho, 'w') as f:
        for valor in lista_valores:
            f.write(f"{valor}\n")

def carregar_valores_financeiros(nome_arquivo):
    caminho = os.path.join('data', nome_arquivo)
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, 'r') as f:
        # Converte de volta para número (float)
        return [float(linha.strip()) for linha in f.readlines()]