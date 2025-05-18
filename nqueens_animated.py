import matplotlib.pyplot as plt
import networkx as nx
from itertools import product, combinations
from matplotlib.animation import FuncAnimation

# Settings
N = 6  # Smaller N for clearer animation
K = 6

def are_compatible(pos1, pos2):
    """Check if two queens do NOT attack each other."""
    r1, c1 = pos1
    r2, c2 = pos2
    return r1 != r2 and c1 != c2 and abs(r1 - r2) != abs(c1 - c2)

def build_compatibility_graph(n):
    """Construct the graph where nodes are positions and edges represent compatibility."""
    G = nx.Graph()
    positions = list(product(range(n), repeat=2))
    G.add_nodes_from(positions)
    for p1, p2 in combinations(positions, 2):
        if are_compatible(p1, p2):
            G.add_edge(p1, p2)
    return G

def draw_board(ax, n):
    """Draw the chessboard background."""
    colors = ['#EEE', '#444']
    for row in range(n):
        for col in range(n):
            color = colors[(row + col) % 2]
            rect = plt.Rectangle([col, n - row - 1], 1, 1, facecolor=color)
            ax.add_patch(rect)

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

# Build graph and find a clique
G = build_compatibility_graph(N)
cliques = list(nx.find_cliques(G))
max_clique = next((c for c in cliques if len(c) == K), None)

# Prepare animation
fig, ax = plt.subplots(figsize=(6, 6))
pos = {node: (node[1] + 0.5, N - node[0] - 0.5) for node in G.nodes}
nodes = list(G.nodes)
edges = list(G.edges)
frames = len(edges) + 10  # some frames for static board

def update(frame):
    ax.clear()
    draw_board(ax, N)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=100, node_color='lightblue')
    if frame > 10:
        edges_to_draw = edges[:frame-10]
        nx.draw_networkx_edges(G, pos, edgelist=edges_to_draw, ax=ax, edge_color="#888")
    if max_clique:
        nx.draw_networkx_nodes(G, pos, nodelist=max_clique, node_color='orange', node_size=200, ax=ax)
        if frame == frames - 1:
            sub = G.subgraph(max_clique)
            nx.draw_networkx_edges(sub, pos, edge_color='red', width=2, ax=ax)
    ax.set_title("Morphing Chessboard into Compatibility Graph")
    ax.axis('off')

ani = FuncAnimation(fig, update, frames=frames, interval=100, repeat=False)
plt.close(fig)
plt.show()
# Save the animation
ani.save('nqueens_compatibility_graph.gif', writer='imagemagick', fps=10)