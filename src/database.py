import json
import os
import ast

# Responsável por todas as operações de I/O (Input/Output), garantindo que os
# dados sobrevivam ao fechamento do programa através de arquivos de texto (.txt).

def salvar_dados(nome_arquivo, lista_itens):
    """
    Salva listas genéricas e dicionários no diretório 'data'.
    """
    if not os.path.exists('data'):
        os.makedirs('data')
        
    caminho = os.path.join('data', nome_arquivo)
    with open(caminho, 'w', encoding='latin-1') as f:
        for item in lista_itens:
            if isinstance(item, dict):
                valores = [str(v) for v in item.values()]
                linha = ",".join(valores)
                f.write(linha + "\n")
            else:
                f.write(str(item) + "\n")

def carregar_dados(nome_arquivo):
    """
    Lê os dados dos arquivos e reconstrói as estruturas (listas/dicionários).
    """
    caminho = os.path.join('data', nome_arquivo)
    lista = []
    if not os.path.exists(caminho): return lista

    with open(caminho, 'r', encoding='latin-1', errors='ignore') as f:
        for linha in f:
            conteudo = linha.strip()
            if not conteudo: continue 

            try:
                if conteudo.startswith('{'):
                    item_convertido = ast.literal_eval(conteudo)
                    lista.append(item_convertido)
                else:
                    if nome_arquivo.startswith('metas'):
                        p = conteudo.split(",")
                        lista.append({'objetivo': p[0], 'valor': p[1]})
                    elif nome_arquivo.startswith('lembretes'):
                        p = conteudo.split(",")
                        lista.append({'conta': p[0], 'data': p[1]})
                    else:
                        lista.append(conteudo)
            except:
                continue 
    return lista

def salvar_valores_financeiros(nome_arquivo, lista_valores):
    """
    Salva valores numéricos (entradas/saídas) em arquivos específicos na pasta 'data'.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    caminho = os.path.join('data', nome_arquivo)
    with open(caminho, 'w') as f:
        for valor in lista_valores:
            f.write(f"{valor}\n")

def carregar_valores_financeiros(nome_arquivo):
    """
    Lê valores do arquivo e os converte de volta para o formato numérico (float).
    """
    caminho = os.path.join('data', nome_arquivo)
    if not os.path.exists(caminho):
        return []

    with open(caminho, 'r') as f:
        return [float(linha.strip()) for linha in f.readlines()]

def carregar_sessao_usuario(usuario_logado):
    """
    Retorna todas as listas financeiras e de metas de um usuário específico.
    """
    metas = carregar_dados(f'metas_{usuario_logado}.txt')
    lembretes = carregar_dados(f'lembretes_{usuario_logado}.txt')
    entradas = carregar_valores_financeiros(f'entradas_{usuario_logado}.txt')
    saidas = carregar_valores_financeiros(f'saidas_{usuario_logado}.txt')
    return metas, lembretes, entradas, saidas
