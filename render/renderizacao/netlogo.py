import pandas as pd

caminho_base = "C:/Users/lucas/Desktop/Metodologia/EstudoDaMalhaEletricaBrasileira/render/renderizacao"

df_nos = pd.read_csv(f"{caminho_base}/subestacao.csv", sep=";")
df_arestas = pd.read_csv(f"{caminho_base}/linha_transmissao.csv", sep=";")

# 1. Limpeza de strings
df_nos['nom_subestacao'] = df_nos['nom_subestacao'].astype(str).str.strip()
df_arestas['nom_subestacao_de'] = df_arestas['nom_subestacao_de'].astype(str).str.strip()
df_arestas['nom_subestacao_para'] = df_arestas['nom_subestacao_para'].astype(str).str.strip()

# 2. Identificar se é Gerador (Procurando termos comuns de usinas no nome)
# Se o nome contiver UHE, UTE, EOL, UFV ou GER, vira 1 (Gerador), senão 0 (Subestação Comum)
df_nos['eh_gerador'] = df_nos['nom_subestacao'].str.upper().str.contains('UHE|UTE|EOL|UFV|GER|USINA').astype(int)

# 3. Tratar a coluna de nível de tensão (remover nulos e garantir que é número)
df_arestas['val_niveltensao_kv'] = pd.to_numeric(df_arestas['val_niveltensao_kv'], errors='coerce').fillna(230)

# Exportar Nós com a nova coluna 'eh_gerador'
nos_netlogo = df_nos[['nom_subestacao', 'val_latitude', 'val_longitude', 'eh_gerador']].dropna()
nos_netlogo.to_csv(f"{caminho_base}/nos_netlogo.txt", sep=",", index=False)

# Exportar Arestas com a coluna de Tensão real
arestas_netlogo = df_arestas[['nom_subestacao_de', 'nom_subestacao_para', 'val_niveltensao_kv']].dropna()
arestas_netlogo.to_csv(f"{caminho_base}/arestas_netlogo.txt", sep=",", index=False)

print("--- NOVOS ARQUIVOS COM TENSÃO E GERADORES GERADOS ---")