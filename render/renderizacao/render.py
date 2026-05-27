import pandas as pd
import networkx as nx

# 1. Carregar os dados (ajuste os caminhos se necessário)
df_nos = pd.read_csv(r"subestacao.csv", sep=";")
df_arestas = pd.read_csv(r"linha_transmissao.csv", sep=";")

# Criar o Grafo Direcionado
G = nx.DiGraph()

# 2. Alimentar os Nós (Subestações)
for index, row in df_nos.iterrows():
    # Usamos o nome como identificador principal (chave) do nó
    nome_no = str(row['nom_subestacao']).strip()
    
    # Pegando as coordenadas que você descobriu que começam com "val"
    # (Ajuste o nome exato se for val_latitude / val_longitude)
    lat = float(row['val_latitude']) if pd.notna(row['val_latitude']) else 0.0
    lon = float(row['val_longitude']) if pd.notna(row['val_longitude']) else 0.0
    
    G.add_node(nome_no, 
               Label=nome_no,  # O Gephi vai ler o nome direto daqui
               latitude=lat, 
               longitude=lon)

# 3. Alimentar as Arestas (Linhas de Transmissão)
for index, row in df_arestas.iterrows():
    # Pegando a origem e destino pelos nomes textuais das colunas que você listou
    origem = str(row['nom_subestacao_de']).strip()
    destino = str(row['nom_subestacao_para']).strip()
    
    # Se ambas as estações existirem no nosso mapa de nós, criamos o link
    if G.has_node(origem) and G.has_node(destino):
        # Aproveitei e adicionei o nível de tensão e o comprimento que vieram no seu CSV
        G.add_edge(origem, destino, 
                   tensao=row['val_niveltensao_kv'],
                   distancia=row['val_comprimento'])

# 4. Exportar para o Gephi
output_path = r"c:\Users\lucas\3D Objects\Algaritmos\Algoritmos-06\malha_eletrica_brasil.gexf"
nx.write_gexf(G, output_path)

print(f"Sucesso! Grafo gerado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
print(f"Arquivo salvo em: {output_path}")