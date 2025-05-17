import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Exemplo de instância de 3-SAT:
# (x1 ∨ !x2 ∨ x3) ∧ (!x1 ∨ x2 ∨ x4) ∧ (!x3 ∨ !x4 ∨ x5)

# Cada literal de cada cláusula vira um nó
clauses = [
    ["x1", "!x2", "x3"],
    ["!x1", "x2", "x4"],
    ["!x3", "!x4", "x5"]
]

# Gera os nomes únicos dos nós: (cláusula_index, literal)
nodes = []
node_colors = []
color_map = ['red', 'green', 'blue']  # uma cor por cláusula
for i, clause in enumerate(clauses):
    for literal in clause:
        nodes.append((i, literal))
        node_colors.append(color_map[i])

# Função para detectar contradição: "x1" vs "!x1"
def are_contradictory(lit1, lit2):
    return lit1 == f"!{lit2}" or f"!{lit1}" == lit2

# Criar grafo vazio
G = nx.Graph()
G.add_nodes_from(nodes)

# Gera as posições dos nós para o layout
pos = nx.spring_layout(G, seed=42)

# Lista de arestas válidas
edges = []
for i, (ci, li) in enumerate(nodes):
    for j, (cj, lj) in enumerate(nodes):
        if ci != cj and not are_contradictory(li, lj) and i < j:
            edges.append(((ci, li), (cj, lj)))

# Função de atualização da animação
fig, ax = plt.subplots(figsize=(8, 6))
drawn_edges = []

def update(num):
    ax.clear()
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800)
    nx.draw_networkx_labels(G, pos, ax=ax, labels={(i, l): l for (i, l) in nodes})
    if num > 0:
        edge = edges[num - 1]
        drawn_edges.append(edge)
    nx.draw_networkx_edges(G, pos, edgelist=drawn_edges, ax=ax, edge_color='gray')
    ax.set_title("Redução de 3-SAT para Clique: passo {}".format(num), fontsize=14)
    ax.axis("off")

ani = animation.FuncAnimation(fig, update, frames=len(edges) + 1, interval=500, repeat=False)

# Salvar como MP4 (se necessário)
output_path = "reducao_3sat_clique.gif"
ani.save(output_path, writer="pillow", fps=2)
# Salvar ultimo frame como imagem
plt.savefig("reducao_3sat_clique_final.png", bbox_inches='tight', dpi=300)
plt.show()



