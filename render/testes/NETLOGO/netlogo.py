import pandas as pd

caminho_base = "C:/Users/discente/Music/EstudoDaMalhaEletricaBrasileira/render/renderizacao"

df_nos = pd.read_csv(f"{caminho_base}/subestacao.csv", sep=";")
df_arestas = pd.read_csv(f"{caminho_base}/linha_transmissao.csv", sep=";")

# Limpando os espaços em branco nos nomes antes de exportar
df_nos['nom_subestacao'] = df_nos['nom_subestacao'].astype(str).str.strip()
df_arestas['nom_subestacao_de'] = df_arestas['nom_subestacao_de'].astype(str).str.strip()
df_arestas['nom_subestacao_para'] = df_arestas['nom_subestacao_para'].astype(str).str.strip()

# Criar arquivo de nós simplificado
nos_netlogo = df_nos[['nom_subestacao', 'val_latitude', 'val_longitude']].dropna()
nos_netlogo.to_csv(f"{caminho_base}/nos_netlogo.txt", sep=",", index=False)

# Criar arquivo de arestas simplificado
arestas_netlogo = df_arestas[['nom_subestacao_de', 'nom_subestacao_para', 'val_niveltensao_kv']].dropna()
arestas_netlogo.to_csv(f"{caminho_base}/arestas_netlogo.txt", sep=",", index=False)

print("--- NOVOS ARQUIVOS LIMPOS GERADOS ---")