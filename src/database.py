import json
import os
import ast

# Responsável por todas as operações de I/O (Input/Output), garantindo que os
# dados sobrevivam ao fechamento do programa através de arquivos de texto (.txt).

def salvar_dados(nome_arquivo, lista_itens):

    """
    Salva listas genéricas e dicionários no diretório 'data'.
    
    Args:
        nome_arquivo (str): Nome do arquivo de destino.
        lista_itens (list): Lista de dados a serem persistidos.
    """
    # Garante que o caminho seja relativo à pasta 'data'
    caminho = os.path.join('data', nome_arquivo)
    # Usamos latin-1 para evitar erros com acentos no Windows
    with open(caminho, 'w', encoding='latin-1') as f:
        for item in lista_itens:
            # Se o item for um dicionário, extrai os valores e os separa por vírgula (CSV manual)
            if isinstance(item, dict):
                valores = [str(v) for v in item.values()]
                linha = ",".join(valores)
                f.write(linha + "\n")
            else:
                # Caso seja uma string ou número simples, escreve diretamente
                f.write(str(item) + "\n")

def carregar_dados(nome_arquivo):

    """
    Lê os dados dos arquivos e reconstrói as estruturas (listas/dicionários).
    
    Returns:
        list: Lista com os dados recuperados ou lista vazia se o arquivo não existir.
    """

    caminho = os.path.join('data', nome_arquivo)
    lista = []
    # Verificação defensiva: evita erro de 'FileNotFound'
    if not os.path.exists(caminho): return lista
    
    with open(caminho, 'r', encoding='latin-1', errors='ignore') as f:
        for linha in f:
            conteudo = linha.strip()
            if not conteudo: continue # Pula linhas vazias
            
            try:
                # LÓGICA DE PARSING (Conversão de texto para objeto)
                
                # Caso 1: O dado está em formato literal de dicionário Python
                if conteudo.startswith('{'):
                    item_convertido = ast.literal_eval(conteudo)
                    lista.append(item_convertido)
                else:
                    # Se for o formato texto normal (separado por vírgula)
                    if nome_arquivo == 'metas.txt':
                        p = conteudo.split(",")
                        lista.append({'objetivo': p[0], 'valor': p[1]})
                    elif nome_arquivo == 'lembretes.txt':
                        p = conteudo.split(",")
                        lista.append({'conta': p[0], 'data': p[1]})
                    else:
                        lista.append(conteudo)
            except:
                continue # Se a linha estiver muito errada, ele só pula e não quebra o programa
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
            # Os valores são convertidos para string apenas para o armazenamento no arquivo
            f.write(f"{valor}\n")

def carregar_valores_financeiros(nome_arquivo):
    """
    Lê valores do arquivo e os converte de volta para o formato numérico (float).
    Essencial para permitir operações matemáticas (soma, média) posteriormente.
    """
    caminho = os.path.join('data', nome_arquivo)
    if not os.path.exists(caminho):
        return []
    
    with open(caminho, 'r') as f:
        # Converte cada linha lida (string) em um número real (float)
        return [float(linha.strip()) for linha in f.readlines()]