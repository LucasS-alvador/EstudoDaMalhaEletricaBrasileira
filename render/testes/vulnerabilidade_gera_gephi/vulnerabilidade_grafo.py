import pandas as pd
import networkx as nx
import copy

# 1. Carregar os dados originais
df_nos = pd.read_csv(r"c:\Users\lucas\3D Objects\render\renderizacao\subestacao.csv", sep=";")
df_arestas = pd.read_csv(r"c:\Users\lucas\3D Objects\render\renderizacao\linha_transmissao.csv", sep=";")

G = nx.Graph() # Usando grafo não-direcionado para análise de ilhas

# Monta o grafo base
for index, row in df_nos.iterrows():
    nome_no = str(row['nom_subestacao']).strip()
    lat = float(row['val_latitude']) if pd.notna(row['val_latitude']) else 0.0
    lon = float(row['val_longitude']) if pd.notna(row['val_longitude']) else 0.0
    
    # Criamos todos os nós inicialmente com o status 'Ativo'
    G.add_node(nome_no, Label=nome_no, latitude=lat, longitude=lon, status="Ativo")

for index, row in df_arestas.iterrows():
    origem = str(row['nom_subestacao_de']).strip()
    destino = str(row['nom_subestacao_para']).strip()
    if G.has_node(origem) and G.has_node(destino):
        G.add_edge(origem, destino, tensao=row['val_niveltensao_kv'])

# -------------------------------------------------------------
# SIMULANDO O ATAQUE E SALVANDO O STATUS
# -------------------------------------------------------------
# Identifica os 5 maiores hubs do país
hubs = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]
nos_ataque = [nó[0] for nó in hubs]

# Criamos uma cópia para simular a quebra e descobrir quem fica isolado
G_simulado = copy.deepcopy(G)
G_simulado.remove_nodes_from(nos_ataque)

# Descobre qual é a maior ilha que sobrou viva (a rede principal)
maior_ilha_viva = max(nx.connected_components(G_simulado), key=len)

# Agora atualizamos os atributos no nosso grafo original G (que tem todos os nós)
for no in G.nodes():
    if no in nos_ataque:
        G.nodes[no]['status'] = 'Causa_Apagao'     # Os nós que nós derrubamos
    elif no in maior_ilha_viva:
        G.nodes[no]['status'] = 'Funcional'        # Continuam recebendo energia
    else:
        G.nodes[no]['status'] = 'Apagado_Isolado'  # Ficaram sem energia (ilhas menores)

# Salva o resultado em um novo arquivo para o Gephi
caminho_saida = r"c:\Users\lucas\3D Objects\render\testes\vulnerabilidade_gera_gephi\vulnerabilidade_resultado.gexf"
nx.write_gexf(G, caminho_saida)
print("Grafo de vulnerabilidade gerado com sucesso!")