import networkx as nx
import copy

# 1. Carregar o grafo gerado anteriormente
caminho_grafo = r"c:\Users\lucas\3D Objects\render\testes\malha_eletrica_brasil.gexf"
# Convertemos para grafo Não-Direcionado (Graph) para facilitar a análise de componentes conectados
G_original = nx.read_gexf(caminho_grafo).to_undirected()

# Fazemos uma cópia para trabalhar sem estragar o arquivo original
G = copy.deepcopy(G_original)

print(f"Estado Inicial do Sistema:")
print(f"Total de Subestações: {G.number_of_nodes()}")
print(f"Total de Linhas de Transmissão: {G.number_of_edges()}")

# O ONS pode ter redes isoladas por padrão (ex: sistemas isolados do Norte). 
# Vamos ver quantas "ilhas" existem originalmente.
ilhas_iniciais = nx.number_connected_components(G)
maior_ilha_inicial = len(max(nx.connected_components(G), key=len))
print(f"Ilhas elétricas iniciais: {ilhas_iniciais}")
print(f"Tamanho da maior rede conectada: {maior_ilha_inicial} subestações\n")

print("--- SIMULANDO APAGÃO DIRECIONADO ---")
print("Removendo os maiores hubs de transmissão do país...\n")

# 2. Identificar os nós mais conectados (Hubs) pelo Grau (Degree)
# Criamos uma lista de tuplas (nome_da_subestacao, numero_de_conexoes) ordenada do maior para o menor
hubs = sorted(G.degree(), key=lambda x: x[1], reverse=True)

# Vamos simular a queda das 5 subestações mais importantes, uma por uma
for i in range(5):
    subestacao_critica, conexoes = hubs[i]
    
    # Remove o nó do grafo simulado
    G.remove_node(subestacao_critica)
    
    # Recalcula o estado da rede após o impacto
    num_ilhas = nx.number_connected_components(G)
    maior_ilha = len(max(nx.connected_components(G), key=len))
    
    print(f"Falha #{i+1}: Subestação [{subestacao_critica}] caiu! (Ela tinha {conexoes} conexões)")
    print(f" -> O país agora ficou dividido em {num_ilhas} blocos isolados.")
    print(f" -> A maior rede restante mantém apenas {maior_ilha} subestações interconectadas.")
    print("-" * 60)

# 3. Medindo o impacto final
perda_percentual = ((maior_ilha_inicial - maior_ilha) / maior_ilha_inicial) * 100
print(f"\nRESULTADO DA ANÁLISE:")
print(f"A queda desses 5 pontos reduziu a principal rede de transmissão em {perda_percentual:.2f}%.")