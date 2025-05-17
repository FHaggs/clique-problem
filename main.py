import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.clique import find_cliques

funcoes = {
    "Ana": ("Montagem", "blue"),
    "Bruno": ("Inspeção", "green"),
    "Carla": ("Manutenção", "gold"),
    "Elisa": ("Programação CNC", "red"),

    "Daniel": ("Montagem", "blue"),
    "Fábio": ("Inspeção", "green"),
    "Gabriel": ("Manutenção", "gold"),
    "Helena": ("Programação CNC", "red"),

    "Igor": ("Montagem", "blue"),
    "Juliana": ("Inspeção", "green"),
    "Katia": ("Manutenção", "gold"),
    "Leo": ("Programação CNC", "red"),
}

# Criando o grafo
G = nx.Graph()
G.add_nodes_from(funcoes.keys())

# Clique garantido: Ana, Bruno, Carla, Elisa
clique_base = [("Ana", "Bruno"), ("Ana", "Carla"), ("Ana", "Elisa"),
               ("Bruno", "Carla"), ("Bruno", "Elisa"),
               ("Carla", "Elisa")]

# Outras conexões para deixar o grafo populado
outras_conexoes = [
    ("Daniel", "Fábio"), ("Daniel", "Gabriel"), ("Daniel", "Helena"),
    ("Fábio", "Gabriel"), ("Fábio", "Helena"),
    ("Gabriel", "Helena"),

    ("Igor", "Juliana"), ("Igor", "Katia"), ("Igor", "Leo"),
    ("Juliana", "Katia"), ("Juliana", "Leo"),
    ("Katia", "Leo"), ("Katia", "Ana"), ("Katia", "Bruno"),

    ("Ana", "Helena"), ("Ana", "Juliana"),
    ("Daniel", "Juliana"),
    ("Elisa", "Fábio"), ("Elisa", "Juliana"), ("Elisa", "Katia")
]

# Adicionando todas as arestas
G.add_edges_from(clique_base + outras_conexoes)
STAFF_SIZE = 4

# Encontrar clique de tamanho 4
cliques = [c for c in find_cliques(G) if len(c) == STAFF_SIZE]
clique_encontrado = None
for c in cliques:
    # Verifica se tem funções distintas
    cores = {funcoes[nome][1] for nome in c}
    if len(cores) == STAFF_SIZE:
        clique_encontrado = c
        break

# Layout do grafo
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(14, 10))

# Cores dos nós com base na função
node_colors = [funcoes[node][1] for node in G.nodes]

# Desenhar todos os nós
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)

# Arestas normais
nx.draw_networkx_edges(G, pos, width=2)

# Destacar o clique
#if clique_encontrado:
    #clique_edges = [(u, v) for u in clique_encontrado for v in clique_encontrado if u != v and G.has_edge(u, v)]
    #nx.draw_networkx_edges(G, pos, edgelist=clique_edges, width=4, edge_color="black")

# Rótulos dos nós com função
labels = {node: f"{node}\n({funcoes[node][0]})" for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=9, font_weight="bold", font_color="black")

plt.title("Grafo de Compatibilidade com Funções Complementares", fontsize=16)
plt.axis("off")
plt.savefig("grafo_clique_funcoes4.png", bbox_inches="tight")
print(f"Clique encontrado de tamanho 4: {clique_encontrado}")
print("Imagem salva como grafo_clique_funcoes4.png")

