import networkx as nx
import matplotlib.pyplot as plt
import os

# Diretório para salvar os frames
os.makedirs("frames", exist_ok=True)

# Cria o grafo
G = nx.Graph()
nodes = ["A", "B", "C", "D", "E"]
edges = [("A", "B"), ("A", "C"), ("B", "C"),
         ("A", "D"), ("B", "D"), ("C", "D"),
         ("E", "A"), ("E", "B")]  # E não faz parte do clique completo
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Layout fixo para consistência visual
pos = nx.spring_layout(G, seed=42)

# Função auxiliar para desenhar e salvar o grafo
def save_step(highlight_nodes=[], highlight_edges=[], step=0, desc=""):
    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, with_labels=True, node_color=[
            "orange" if n in highlight_nodes else "lightgray" for n in G.nodes()],
            edge_color=["blue" if e in highlight_edges or (e[1], e[0]) in highlight_edges else "gray" for e in G.edges()],
            node_size=1000, width=2, font_size=12)
    plt.title(f"Passo {step}: {desc}")
    plt.savefig(f"frames/step_{step}.png")
    plt.close()

# Passo 1: Grafo inicial
save_step(step=1, desc="Grafo com operadores e compatibilidades")

# Passo 2: Encontrar uma dupla
save_step(highlight_nodes=["A", "B"], highlight_edges=[("A", "B")], step=2,
          desc="Escolhendo uma dupla compatível: A e B")

# Passo 3: Formar um trio
save_step(highlight_nodes=["A", "B", "C"], highlight_edges=[
          ("A", "B"), ("A", "C"), ("B", "C")], step=3,
          desc="Adicionando C, que é compatível com A e B")

# Passo 4: Formar um clique de 4
save_step(highlight_nodes=["A", "B", "C", "D"], highlight_edges=[
          ("A", "B"), ("A", "C"), ("B", "C"),
          ("A", "D"), ("B", "D"), ("C", "D")], step=4,
          desc="Adicionando D: todos compatíveis — clique de tamanho 4!")

# Passo 5: E não entra no clique
save_step(highlight_nodes=["E"], step=5,
          desc="E não pode entrar, falta compatibilidade com C e D")

