import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')

# Vamos reusar a mesma construção do grafo baseada em uma fórmula 3-SAT
# Fórmula: (x1 ∨ ¬x2 ∨ x3) ∧ (¬x1 ∨ x2 ∨ x4) ∧ (¬x3 ∨ ¬x4 ∨ x5)
clauses = [
    ["x1", "¬x2", "x3"],
    ["¬x1", "x2", "x4"],
    ["¬x3", "¬x4", "x5"]
]

# Construir grafo
G = nx.Graph()

# Mapeia cada literal a um nó com (clause_idx, literal)
nodes = []
for i, clause in enumerate(clauses):
    for literal in clause:
        node = (i, literal)
        nodes.append(node)
        G.add_node(node)

# Adiciona arestas entre pares de literais de cláusulas diferentes e não contraditórios
def is_compatible(l1, l2):
    var1 = l1.replace("¬", "")
    var2 = l2.replace("¬", "")
    return not (var1 == var2 and ("¬" in l1) != ("¬" in l2))

for u, v in combinations(nodes, 2):
    i, lit1 = u
    j, lit2 = v
    if i != j and is_compatible(lit1, lit2):
        G.add_edge(u, v)

# Agora vamos procurar um clique de tamanho igual ao número de cláusulas (3)
clique_size = len(clauses)
found_clique = None

for clique in nx.find_cliques(G):
    if len(clique) == clique_size:
        found_clique = clique
        break

print(found_clique)
import matplotlib.pyplot as plt

# Preparar o layout para visualização
pos = nx.spring_layout(G, seed=42)

# Separar os nós do clique e os demais
clique_nodes = set(found_clique)
node_colors = ['orange' if node in clique_nodes else 'lightgray' for node in G.nodes()]
edge_colors = ['red' if (u in clique_nodes and v in clique_nodes) else 'gray' for u, v in G.edges()]

# Desenhar os nós
plt.figure(figsize=(10, 6))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800)
nx.draw_networkx_labels(G, pos, labels={node: node[1] for node in G.nodes()}, font_size=12)

# Desenhar as arestas
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)

# Título
plt.title("Grafo construído a partir da fórmula 3-SAT\nClique de tamanho 3 em destaque", fontsize=14)
plt.axis('off')
plt.savefig("sat_res.png", bbox_inches='tight', dpi=300)
