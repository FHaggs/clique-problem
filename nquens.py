import matplotlib.pyplot as plt
import networkx as nx
from itertools import product, combinations

# -- Settings --
N = 8  # Board size
K = 8  # Clique size to look for

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

def draw_board(n):
    """Draw the empty chessboard."""
    fig, ax = plt.subplots()
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
    plt.title("Chessboard")
    return fig, ax

def draw_graph(G, k_clique=None, n=8):
    """Visualize the compatibility graph, highlighting a K-clique if found."""
    pos = {node: (node[1], n - node[0] - 1) for node in G.nodes}
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_size=100, node_color='lightblue', with_labels=False, edge_color="#CCC")
    
    if k_clique:
        nx.draw_networkx_nodes(G, pos, nodelist=k_clique, node_color='orange', node_size=200)
        sub = G.subgraph(k_clique)
        nx.draw_networkx_edges(sub, pos, edge_color='red', width=2)
        plt.title(f"{len(k_clique)}-Clique Found")
    else:
        plt.title("Compatibility Graph")
    plt.axis('off')
    plt.show()

# -- Main Execution --
G = build_compatibility_graph(N)

# Draw the board
draw_board(N)
plt.show()

# Draw the graph
draw_graph(G, n=N)

# Try to find a clique of size K
cliques = list(nx.find_cliques(G))
max_clique = next((c for c in cliques if len(c) == K), None)

if max_clique:
    draw_graph(G, k_clique=max_clique, n=N)
    print(f"Found a clique of size {K}:", max_clique)
else:
    print(f"No clique of size {K} found.")

