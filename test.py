import networkx as nx
import matplotlib.pyplot as plt

# Define your graph
G = nx.Graph()
edges = [(0, 1), (1, 2)]
colors = [("red", "green"), ("blue", "red")]  # edge-end colors

# Add nodes and edges to graph
G.add_edges_from(edges)

# Get positions for nodes
pos = nx.spring_layout(G)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color="lightgray", edgecolors="black")
nx.draw_networkx_labels(G, pos)

# Draw each edge as two colored segments
for (u, v), (color_u, color_v) in zip(edges, colors):
    # Get node positions
    x1, y1 = pos[u]
    x2, y2 = pos[v]

    # Midpoint
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2

    # Draw first half
    plt.plot([x1, xm], [y1, ym], color=color_u, linewidth=2)

    # Draw second half
    plt.plot([xm, x2], [ym, y2], color=color_v, linewidth=2)

plt.axis("off")
plt.show()
