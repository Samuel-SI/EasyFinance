import json
import os
import ast

def salvar_dados(nome_arquivo, lista_itens):
    caminho = os.path.join('data', nome_arquivo)
    # Usamos latin-1 para evitar erros com acentos no Windows
    with open(caminho, 'w', encoding='latin-1') as f:
        for item in lista_itens:
            if isinstance(item, dict):
                valores = [str(v) for v in item.values()]
                linha = ",".join(valores)
                f.write(linha + "\n")
            else:
                f.write(str(item) + "\n")

def carregar_dados(nome_arquivo):
    caminho = os.path.join('data', nome_arquivo)
    lista = []
    if not os.path.exists(caminho): return lista
    
    with open(caminho, 'r', encoding='latin-1', errors='ignore') as f:
        for linha in f:
            conteudo = linha.strip()
            if not conteudo: continue
            
            try:
                # Tenta converter a linha se ela estiver salva como {'chave': 'valor'}
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